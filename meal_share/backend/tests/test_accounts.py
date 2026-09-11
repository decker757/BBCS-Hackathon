"""Account and meal authorization checks with only disposable synthetic files."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from werkzeug.security import generate_password_hash

SOURCE = Path(__file__).resolve().parents[1] / 'app.py'
HEADERS = {'X-Meal-Share-Request': '1'}


class AccountTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_cwd = Path.cwd()
        self.temp = tempfile.TemporaryDirectory(prefix='meal-share-test-')
        os.chdir(self.temp.name)
        self.environment = patch.dict(os.environ, {'MEAL_SHARE_DATA_DIR': self.temp.name})
        self.environment.start()
        Path('users').mkdir()
        Path('meals').mkdir()
        self.hashed = generate_password_hash('synthetic-test-password')
        Path('users/business.txt').write_text('\n'.join(json.dumps({'username': name, 'password': self.hashed, 'businessemail': name+'@example.invalid'}) for name in ['owner', 'other'])+'\n')
        Path('users/drivers.txt').write_text(json.dumps({'username': 'driver', 'password': self.hashed})+'\n')
        Path('meals/owner_meals.txt').write_text(json.dumps({'dishName': 'Rice', 'mealType': 'Vegetarian', 'quantity': 3})+'\n')
        spec = importlib.util.spec_from_file_location('meal_share_fixture', SOURCE)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.module.app.config.update(TESTING=True, SECRET_KEY='synthetic-session-fixture-only', SESSION_COOKIE_SECURE=False)
        self.client = self.module.app.test_client()
        self.network = patch.object(self.module.requests, 'get', side_effect=AssertionError('External provider request forbidden in account checks'))
        self.network.start()

    def tearDown(self) -> None:
        self.network.stop()
        self.environment.stop()
        os.chdir(self.original_cwd)
        self.temp.cleanup()

    def login(self, username: str = 'owner', role: str = 'business'):
        return self.client.post('/api/'+role+'/login', json={'username': username, 'password': 'synthetic-test-password'}, headers=HEADERS)

    def test_unauthenticated_create(self) -> None:
        self.assertEqual(self.client.post('/meals/available/owner', json={'dishName': 'Soup', 'mealType': 'Vegetarian', 'quantity': 2}, headers=HEADERS).status_code, 401)

    def test_unauthenticated_read(self) -> None:
        self.assertEqual(self.client.get('/business/updatemeals/owner').status_code, 401)

    def test_unauthenticated_update(self) -> None:
        self.assertEqual(self.client.put('/business/updatemeals/owner', json={'dishName': 'Rice', 'newQuantity': 8}, headers=HEADERS).status_code, 401)

    def test_owner_flow_and_zero_quantity(self) -> None:
        self.assertEqual(self.login().status_code, 200)
        self.assertEqual(self.client.post('/meals/available/owner', json={'dishName': 'Soup', 'mealType': 'Vegetarian', 'quantity': '2'}, headers=HEADERS).status_code, 201)
        self.assertEqual(self.client.put('/business/updatemeals/owner', json={'dishName': 'Rice', 'newQuantity': 0}, headers=HEADERS).status_code, 200)
        meals = self.client.get('/business/updatemeals/owner').get_json()
        self.assertEqual([meal['quantity'] for meal in meals], [0, 2])

    def test_other_account_cannot_read_or_change_meals(self) -> None:
        self.login('other')
        original = Path('meals/owner_meals.txt').read_bytes()
        for method in ['get', 'post', 'put']:
            path = '/meals/available/owner' if method == 'post' else '/business/updatemeals/owner'
            response = getattr(self.client, method)(path, json={'dishName': 'Rice', 'mealType': 'V', 'quantity': 5, 'newQuantity': 5}, headers=HEADERS)
            self.assertEqual(response.status_code, 403)
        self.assertEqual(Path('meals/owner_meals.txt').read_bytes(), original)

    def test_driver_cannot_edit_business_meals(self) -> None:
        self.assertEqual(self.login('driver', 'driver').status_code, 200)
        self.assertEqual(self.client.put('/business/updatemeals/owner', json={'dishName': 'Rice', 'newQuantity': 8}, headers=HEADERS).status_code, 403)

    def test_session_identity_and_logout(self) -> None:
        response = self.login()
        cookie = response.headers.get('Set-Cookie', '')
        self.assertIn('HttpOnly', cookie)
        self.assertIn('SameSite=Lax', cookie)
        self.assertEqual(self.client.get('/api/session').get_json(), {'username': 'owner', 'role': 'business'})
        self.assertEqual(self.client.post('/api/logout', headers=HEADERS).status_code, 200)
        self.assertEqual(self.client.get('/business/updatemeals/owner').status_code, 401)

    def test_secure_cookie_and_private_cache(self) -> None:
        self.module.app.config['SESSION_COOKIE_SECURE'] = True
        response = self.login()
        self.assertIn('Secure', response.headers.get('Set-Cookie', ''))
        self.assertIn('no-store', response.headers.get('Cache-Control', ''))

    def test_missing_session_key_fails_closed(self) -> None:
        self.module.app.config['SECRET_KEY'] = None
        self.assertEqual(self.login().status_code, 503)
        self.assertEqual(self.client.post('/api/logout', headers=HEADERS).status_code, 503)

    def test_forged_session_is_anonymous(self) -> None:
        self.client.set_cookie('session', 'forged-unsigned-owner-session')
        self.assertEqual(self.client.get('/business/updatemeals/owner').status_code, 401)

    def test_cross_origin_and_simple_form_requests_rejected(self) -> None:
        self.assertEqual(self.client.post('/api/business/login', json={'username': 'owner', 'password': 'synthetic-test-password'}).status_code, 403)
        self.assertEqual(self.client.post('/api/business/login', json={'username': 'owner', 'password': 'synthetic-test-password'}, headers={**HEADERS, 'Origin': 'https://untrusted.example.invalid'}).status_code, 403)

    def test_allowed_local_origin_can_use_cookies(self) -> None:
        response = self.client.post('/api/business/login', json={'username': 'owner', 'password': 'synthetic-test-password'}, headers={**HEADERS, 'Origin': 'http://localhost:3000'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), 'http://localhost:3000')
        self.assertEqual(response.headers.get('Access-Control-Allow-Credentials'), 'true')

    def test_malformed_registration_bodies_do_not_write(self) -> None:
        for role in ['driver', 'business']:
            before = Path('users/'+('drivers' if role == 'driver' else 'business')+'.txt').read_bytes()
            for body in [None, [], 'text', {'password': 'only-one-field'}, {'username': []}]:
                with self.subTest(role=role, body_type=type(body).__name__):
                    response = self.client.post('/api/'+role+'/register', data=json.dumps(body), content_type='application/json', headers=HEADERS)
                    self.assertEqual(response.status_code, 400)
            self.assertEqual(Path('users/'+('drivers' if role == 'driver' else 'business')+'.txt').read_bytes(), before)

    def test_unsafe_registration_username_rejected(self) -> None:
        data = {name: 'synthetic' for name in ['firstname', 'lastname', 'role', 'businessname', 'businessemail', 'address', 'postal', 'password']}
        for name in ['../outside', 'nested/name', 'nested\\name', 'name:stream']:
            with self.subTest(name=name):
                response = self.client.post('/api/business/register', json={**data, 'username': name}, headers=HEADERS)
                self.assertEqual(response.status_code, 400)

    def test_invalid_quantities_do_not_write(self) -> None:
        self.login()
        before = Path('meals/owner_meals.txt').read_bytes()
        for quantity in [-1, True, {}, [], 1.5, '2x', '']:
            with self.subTest(quantity=quantity):
                response = self.client.put('/business/updatemeals/owner', json={'dishName': 'Rice', 'newQuantity': quantity}, headers=HEADERS)
                self.assertEqual(response.status_code, 400)
        self.assertEqual(Path('meals/owner_meals.txt').read_bytes(), before)

    def test_missing_dish_preserves_file(self) -> None:
        self.login()
        before = Path('meals/owner_meals.txt').read_bytes()
        self.assertEqual(self.client.put('/business/updatemeals/owner', json={'dishName': 'Absent', 'newQuantity': 1}, headers=HEADERS).status_code, 404)
        self.assertEqual(Path('meals/owner_meals.txt').read_bytes(), before)

    def test_registration_retains_password_hash_and_creates_meal_file(self) -> None:
        data = {name: 'synthetic' for name in ['firstname', 'lastname', 'role', 'businessname', 'address', 'postal']}
        data.update(username='new-business', password='synthetic-test-password', businessemail='new@example.invalid')
        self.assertEqual(self.client.post('/api/business/register', json=data, headers=HEADERS).status_code, 201)
        record = json.loads(Path('users/business.txt').read_text().splitlines()[-1])
        self.assertNotEqual(record['password'], data['password'])
        self.assertTrue(Path('meals/new-business_meals.txt').exists())
        self.assertEqual(self.login('new-business').status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
