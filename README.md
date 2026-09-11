# NomNomNetwork — BBCS Hackathon

NomNomNetwork connects food businesses offering meals with delivery riders. The current application is the React frontend in `meal_share/frontend` and the Flask API in `meal_share/backend/app.py`.

## Run locally

Use Node 22 and Python 3.12. In a PowerShell terminal at the repository root:

```powershell
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r meal_share/backend/requirements.txt
$env:FLASK_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:SESSION_COOKIE_SECURE = "false"
$env:MEAL_SHARE_DATA_DIR = Join-Path $env:TEMP "nomnom-local-data"
python meal_share/backend/app.py
```

This example puts new demo records in a separate temporary directory. Keep that directory if its demo data matters. Without `MEAL_SHARE_DATA_DIR`, the API uses the existing `meal_share/backend/users` and `meal_share/backend/meals` files. Changing the configured directory does not copy or migrate records.

In a second terminal:

```powershell
cd meal_share/frontend
npm ci --ignore-scripts --no-fund
npm start
```

Open `http://localhost:3000`. The development proxy forwards relative API requests to `http://127.0.0.1:5000`. Business accounts can register, sign in, add meals and update their quantities, including zero. The editor restores its account from the server session after reload. Riders have a separate sign-in flow and cannot manage a business's meals.

## Hosting and configuration

No production runtime has been mapped for this repository in the portfolio's accessible Vercel projects. Publishing source or building the frontend does not establish a working hosted Flask API. The local file store needs persistent storage; an ephemeral serverless filesystem cannot safely replace it.

Build the frontend with `npm run build` from `meal_share/frontend`. Serve `build/` and route `/api/*`, `/meals/*` and `/business/*` to the API on the same HTTPS origin. Only frontend routes should fall back to `index.html`. Alternatively, set `REACT_APP_API_BASE_URL` at build time to a compatible API origin and list the frontend's exact origin in `FRONTEND_ORIGINS`. Cookies use `SameSite=Lax`, so unrelated cross-site domains are not supported by simply enabling CORS.

The API requires a stable, private `FLASK_SECRET_KEY` to sign sessions. Login and logout return a controlled unavailable response if it is missing. Production cookies are Secure and HttpOnly by default; the `SESSION_COOKIE_SECURE=false` override is for local HTTP. Sessions expire after eight hours and are not renewed by ordinary reads. Logout clears the current browser's session cookie; this signed-cookie design does not provide server-side revocation of a copied cookie.

Set `FRONTEND_ORIGINS` to the public frontend's exact HTTPS origin, including when a reverse proxy forwards requests to a different internal API address. Keep the secret key in the host's private configuration and preserve it across ordinary restarts.

Mutating requests require `X-Meal-Share-Request: 1`. Requests carrying an Origin header must come from the same origin or an explicit `FRONTEND_ORIGINS` entry. The bundled client supplies the header and includes cookies. Do not use wildcard credential origins or expose the development server as a production server.

Maps require a restricted browser `REACT_APP_GOOGLE_MAPS_API_KEY` and a private server `GOOGLE_MAPS_API_KEY`. Account and meal checks do not require either. The location endpoint still geocodes businesses on demand; caching, provider quotas and total request budgeting remain follow-up work. The per-call connection/read timeouts are not a total batch deadline.

## Checks

Backend authorization checks use disposable synthetic records:

```powershell
python -m unittest discover -s meal_share/backend/tests -p "test_*.py" -v
```

From `meal_share/frontend`, run:

```powershell
$env:CI = "true"
npm test -- --watch=false --runInBand
npm run build
```

For the real browser fixture, run from the repository root after building:

```powershell
python -m pip install -r meal_share/backend/requirements-test.txt
python -m playwright install chromium
python meal_share/backend/tests/browser_accounts.py
```

The browser fixture serves the built UI with the real API on loopback, uses temporary account/meal records, blocks external provider requests and checks desktop/mobile login, ownership, saving, session restoration and logout. Reports and screenshots go to the ignored `meal_share/browser-results/` directory. CI runs these checks for changes to the active application on pull requests and main.

CRA's Jest 27 resolver needs an explicit mapping for React Router's `react-router/dom` package export; the mapping loads the real installed implementation. The Babel preset's otherwise undeclared private-property plugin is also listed explicitly. These keep the current toolchain reproducible while its replacement remains open. See [CRA's supported Jest configuration](https://create-react-app.dev/docs/running-tests/#configuration).

## Data preservation and remaining work

Existing account/meal files, `backup(plsdontdelete)/` and historical entry points are preserved. Only `meal_share/backend/app.py` is the current supported API entry point. Its meal writes share an in-process lock and quantity updates replace a complete file atomically; multi-process registration/writes, duplicate dish identity, abuse limits and a lossless Supabase migration remain open. This release does not move or delete data and does not make the whole application production-ready. The Create React App build chain also has 30 remaining dependency audit entries (none critical), down from 66 before compatible updates. Express constrains its query-string dependency and JSONPath pins Underscore; broader tooling replacement remains open. The previously empty About route is restored and covered by navigation/browser checks.

## Portfolio upkeep task list — 2026-09-11

- [x] Reproduce missing login/ownership checks and malformed registration/quantity inputs using synthetic files.
- [x] Add signed sessions, ownership and request-origin protection while preserving records and backups.
- [x] Verify configurable API routing, backend/client builds and real browser account flows.
- [ ] Pass hosted checks, publish reviewed source and record the production hosting limits in the portfolio plans.
