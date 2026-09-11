"""Exercise the built UI against this Flask API using disposable fixture records.

No real accounts, maps provider, deployment or existing user/meal files are used.
Run after the frontend build: python meal_share/backend/tests/browser_accounts.py
"""
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from unittest.mock import patch
from urllib.parse import urlparse

from flask import abort, send_from_directory
from playwright.sync_api import expect, sync_playwright
from werkzeug.security import generate_password_hash
from werkzeug.serving import make_server, WSGIRequestHandler

MEAL_SHARE = Path(__file__).resolve().parents[2]
BUILD = MEAL_SHARE / 'frontend/build'
REPORT_DIR = Path(os.getenv('MEAL_SHARE_BROWSER_REPORT', str(MEAL_SHARE / 'browser-results')))
HEADERS = {'X-Meal-Share-Request': '1'}
PASSWORD = 'synthetic-browser-password'


class QuietHandler(WSGIRequestHandler):
    def log(self, kind, message, *args):
        pass


def run():
    assert (BUILD / 'index.html').is_file(), 'Build the frontend before browser checks'
    expect.set_options(timeout=30000)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix='meal-share-browser-') as directory:
        fixture = Path(directory)
        (fixture / 'users').mkdir()
        (fixture / 'meals').mkdir()
        password_hash = generate_password_hash(PASSWORD)
        (fixture / 'users/business.txt').write_text(json.dumps({
            'username': 'owner', 'password': password_hash,
            'businessemail': 'owner@example.invalid',
        }) + '\n', encoding='utf-8')
        (fixture / 'users/drivers.txt').write_text(json.dumps({
            'username': 'driver', 'password': password_hash,
        }) + '\n', encoding='utf-8')
        with patch.dict(os.environ, {
            'MEAL_SHARE_DATA_DIR': directory,
            'FLASK_SECRET_KEY': 'synthetic-browser-session-key-only',
            'SESSION_COOKIE_SECURE': 'false',
            'GOOGLE_MAPS_API_KEY': '',
        }):
            spec = importlib.util.spec_from_file_location('meal_share_browser_fixture', MEAL_SHARE / 'backend/app.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        app = module.app
        app.config.update(TESTING=True)
        # Static serving belongs to this local test harness, not the API runtime.
        app.static_folder = str(BUILD / 'static')

        @app.get('/')
        @app.get('/<path:path>')
        def frontend(path=''):
            if path.startswith(('api/', 'business/', 'meals/')):
                abort(404)
            asset = BUILD / path
            if asset.is_file() and asset.resolve().is_relative_to(BUILD.resolve()):
                return send_from_directory(BUILD, path)
            return send_from_directory(BUILD, 'index.html')

        server = make_server('127.0.0.1', 0, app, threaded=True, request_handler=QuietHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        origin = f'http://127.0.0.1:{server.server_port}'
        try:
            with patch.object(module.requests, 'get', side_effect=AssertionError('External provider request forbidden')), sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                try:
                    for width in (1440, 390):
                        (fixture / 'meals/owner_meals.txt').write_text(json.dumps({
                            'dishName': 'Rice', 'mealType': 'Vegetarian', 'quantity': 3,
                        }) + '\n', encoding='utf-8')
                        context = browser.new_context(viewport={'width': width, 'height': 900}, service_workers='block')
                        external = []

                        def local_only(route):
                            if urlparse(route.request.url).netloc == urlparse(origin).netloc:
                                route.continue_()
                            else:
                                external.append(urlparse(route.request.url).hostname)
                                route.abort()

                        context.route('**/*', local_only)
                        page = context.new_page()
                        page.set_default_timeout(30000)
                        errors = []
                        page.on('pageerror', lambda error: errors.append(str(error)))

                        def passed(name):
                            results.append({'width': width, 'check': name, 'passed': True})
                            print(f'{width}px: {name}', flush=True)

                        def login(role='business', username='owner'):
                            page.goto(origin + '/' + role + 'login')
                            page.get_by_label('Username:').fill(username)
                            page.get_by_label('Password:').fill(PASSWORD)
                            page.get_by_role('button', name='Login', exact=True).click()
                            page.wait_for_url(origin + '/' + role + 'about')

                        page.goto(origin + '/about')
                        expect(page.get_by_role('heading', name='About NomNomNetwork')).to_be_visible()
                        page.get_by_role('link', name='Back to home').click()
                        page.wait_for_url(origin + '/')
                        passed('About route renders and returns home')

                        page.goto(origin + '/providerupdate')
                        page.wait_for_url(origin + '/businesslogin')
                        passed('anonymous direct editor opens sign-in')
                        page.get_by_label('Username:').fill('owner')
                        page.get_by_label('Password:').fill('incorrect-fixture-password')
                        page.get_by_role('button', name='Login', exact=True).click()
                        expect(page.get_by_role('alert')).to_contain_text('Invalid username or password')
                        passed('bad credentials remain visible')
                        login()
                        expect(page.get_by_text('Signed in as owner', exact=True)).to_be_visible()
                        page.get_by_label('Dish name', exact=True).fill('Soup')
                        page.get_by_label('Meal type', exact=True).fill('Vegetarian')
                        page.get_by_label('Quantity', exact=True).fill('2')
                        page.get_by_role('button', name='Add Meal', exact=True).click()
                        expect(page.get_by_role('button', name='Edit Soup')).to_be_visible()
                        passed('signed-in add persists')
                        page.get_by_role('button', name='Edit Rice').click()
                        page.get_by_label('Quantity for Rice').fill('0')
                        page.get_by_role('button', name='Save', exact=True).click()
                        expect(page.get_by_role('listitem').filter(has=page.get_by_role('button', name='Edit Rice'))).to_contain_text('Quantity: 0')
                        page.reload()
                        expect(page.get_by_text('Signed in as owner', exact=True)).to_be_visible()
                        expect(page.get_by_role('listitem').filter(has=page.get_by_role('button', name='Edit Rice'))).to_contain_text('Quantity: 0')
                        passed('zero quantity and session survive reload')

                        fail_refresh = [True]

                        def refresh_failure(route):
                            if route.request.method == 'GET' and fail_refresh[0]:
                                fail_refresh[0] = False
                                route.fulfill(status=503, content_type='application/json', body='{"message":"Synthetic refresh failure"}')
                            else:
                                route.fallback()

                        page.route('**/business/updatemeals/owner', refresh_failure)
                        page.get_by_label('Dish name', exact=True).fill('Noodles')
                        page.get_by_label('Meal type', exact=True).fill('Vegetarian')
                        page.get_by_label('Quantity', exact=True).fill('1')
                        page.get_by_role('button', name='Add Meal', exact=True).click()
                        expect(page.get_by_role('alert')).to_contain_text('Your changes were saved, but the list could not refresh')
                        expect(page.get_by_label('Dish name', exact=True)).to_have_value('')
                        page.reload()
                        expect(page.get_by_role('button', name='Edit Noodles')).to_have_count(1)
                        passed('acknowledged save stays distinct from failed list refresh')
                        overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                        assert not overflow, f'Editor overflows at {width}px'
                        page.screenshot(path=str(REPORT_DIR / f'editor-{width}.png'), full_page=False)
                        passed('editor fits viewport')

                        page.route('**/api/logout', lambda route: route.fulfill(status=503, content_type='application/json', body='{"message":"Synthetic logout failure"}'))
                        page.get_by_role('button', name='Logout').click()
                        expect(page.get_by_role('alert')).to_contain_text('Unable to sign out')
                        assert context.request.get(origin + '/api/session').json()['username'] == 'owner'
                        page.unroute('**/api/logout')
                        page.get_by_role('button', name='Logout').click()
                        page.wait_for_url(origin + '/')
                        assert context.request.get(origin + '/business/updatemeals/owner').status == 401
                        passed('failed logout offers retry; successful logout revokes browser access')

                        login()
                        expect(page.get_by_role('button', name='Edit Rice')).to_be_visible()
                        context.clear_cookies()
                        page.get_by_role('button', name='Edit Rice').click()
                        page.get_by_label('Quantity for Rice').fill('7')
                        page.get_by_role('button', name='Save', exact=True).click()
                        expect(page.get_by_role('alert')).to_contain_text('Your session has expired')
                        expect(page.get_by_role('link', name='Sign in', exact=True)).to_be_visible()
                        assert json.loads((fixture / 'meals/owner_meals.txt').read_text().splitlines()[0])['quantity'] == 0
                        passed('expired session rejects edits without changing data')

                        login('driver', 'driver')
                        assert context.request.put(origin + '/business/updatemeals/owner', headers=HEADERS, data={'dishName': 'Rice', 'newQuantity': 9}).status == 403
                        page.get_by_role('button', name='Logout').click()
                        page.wait_for_url(origin + '/')
                        assert context.request.get(origin + '/api/session').json()['username'] is None
                        passed('driver sign-in cannot edit business meals and signs out')
                        assert not errors, errors
                        assert not external, external
                        passed('no browser exceptions or external requests')
                        context.close()
                        print(f'{width}px: account browser checks passed', flush=True)
                finally:
                    browser.close()
        finally:
            server.shutdown()
            thread.join(timeout=10)
            server.server_close()
            assert not thread.is_alive(), 'Fixture server did not stop'
    report = {'checks': results, 'passed': len(results), 'production_requests': 0, 'existing_records_used': False}
    (REPORT_DIR / 'accounts.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'passed': len(results), 'report': str(REPORT_DIR / 'accounts.json')}))


if __name__ == '__main__':
    run()
