# PRD: NomNomNetwork — BBCS Hackathon

## Product

Food businesses offer meals to delivery riders. A business can register, sign in, list its meals and change available quantities. Riders can register, sign in and browse business meal locations. The current code does not implement reservations, inventory claims, payment or delivery dispatch.

## Current architecture

- `meal_share/frontend/`: React 18, React Router and Create React App.
- `meal_share/backend/app.py`: Flask API with signed session cookies, business ownership checks and explicit credential origins.
- `meal_share/backend/users/` and `meal_share/backend/meals/`: existing JSON-lines record storage, configurable through `MEAL_SHARE_DATA_DIR`.
- Google Maps: optional browser map and server geocoding integration.
- `backup(plsdontdelete)/`: historical development backup; preserved.

The frontend uses relative API routes by default. Local development uses its configured proxy; production requires a correctly routed persistent API. See README for setup, session configuration and checks. No production host has been verified for this repository among the accessible portfolio projects.

## Maintenance behavior

Meal management requires the business's signed session. Anonymous requests receive 401 and another account or a rider receives 403. Reloading the editor restores server identity; logout clears the browser's cookie. Input validation rejects malformed registration bodies, unsafe usernames and invalid quantities, while accepting zero. Failed updates leave the previous complete meal file in place.

Synthetic backend and desktop/mobile browser checks cover the account and meal workflows without using existing records or calling external providers. CI checks active application changes before source publication.

## Open work

Preserve all existing records during any future Supabase migration. Persistent hosting, multi-process data consistency, unique meal identifiers, abuse controls, geocoding caching/quotas, legacy frontend tooling and wider UX remain separate maintenance items. The existing UI belongs to the hackathon project; Prawn-family branding does not automatically rename it.
