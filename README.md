# PeopleHub backend

## Run locally with Docker

Install and start Docker Desktop (or Docker Engine with Docker Compose 2.32+).
From this directory:

```sh
cp .env.example .env
docker compose -f docker-compose-local.yml up --build --watch
```

On Windows PowerShell, use `Copy-Item .env.example .env` to copy the file.
The example environment values work for local development. Django runs at
http://localhost:8000 and the admin is at http://localhost:8000/admin/.
The watched command applies database migrations before starting Django.
Keep this command running while developing. Compose Watch copies saved source
changes into the container. A separate `watchfiles` process restarts Django after
Python edits, including when an invalid edit to `settings.py` crashes Django.
Fix the error and save again to recover automatically. Django's built-in
reloader is disabled so only one watcher manages the application process.
This avoids relying on Docker Desktop bind-mount synchronization. Refresh your
browser after saving to see the updated response. Changes to `requirements.txt`
or `Dockerfile` automatically rebuild the web service. Files excluded by
`.dockerignore` (including `.env`) are not synced. After changing `.env`, run
`docker compose -f docker-compose-local.yml up --build --watch --force-recreate`
again to load the updated environment. New migration files are applied when the
watched command restarts; generate them with
`docker compose -f docker-compose-local.yml exec web python manage.py makemigrations`.
Compose uses the `db` and `redis` service names for container connections.

Create an admin account in a second terminal:

```sh
docker compose -f docker-compose-local.yml exec web python manage.py createsuperuser
```

Stop the containers:

```sh
docker compose -f docker-compose-local.yml down
```

PostgreSQL data persists in the `pgdata` volume. The host PostgreSQL port can
be changed with `POSTGRES_PORT` in `.env` if port 5432 is already occupied.
Redis publishes port 6379; Django publishes port 8000.

This configuration uses Django's development server and is intended for local
development. Use a production application server and production settings before
public deployment. Do not commit `.env`.

## Simple user authentication

The API uses usernames and passwords with JWT access tokens.

- `POST /api/v1/users/register/`: send `username`, `email`, `password`, and optionally `phone`.
- `POST /api/v1/users/login/`: send `username` and `password`; returns `access` and `refresh` tokens.
- `GET /api/v1/users/me/`: send `Authorization: Bearer <access>` to get your profile.
- `POST /api/v1/users/refresh/`: send `{"refresh": "<refresh token>"}` to obtain a new access token. Store the returned refresh token too, since refresh tokens rotate.

Apply migrations before using authentication. If this database already has migrations
applied with Django's default User model, switching to the custom User requires a
planned database migration; do not delete existing data or migration history.

Run authentication tests with:

```sh
docker compose -f docker-compose-local.yml exec web python manage.py test PeopleHub.apps.users
```
