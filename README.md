
This project uses Docker to run:
- A **Django** backend with Pipenv
- A **PostGIS** database
    - PostGIS extends the capabilities of the PostgreSQL relational database by adding support for storing, indexing, and querying geospatial data.
- A **Next.js** frontend for the user interface

---

## Getting Started

### Start everything (backend + frontend + database)

```bash
make up
```

This will:
- Build the Django container
- Build the Next.js frontend container
- Start the PostGIS database
- Run:
  - Django server at http://localhost:8000
  - Next.js dev server at http://localhost:3000

#### When starting the app for the first time, or after destroying the docker containers, synchronize the database state with the current set of models and migrations by running this command in another terminal:

```bash
make migrate
```

---

### Swagger

Once the backend is running view the api endpoints at:

```
localhost:8000/swagger
```

---

## Development Server Commands

Start only the backend:

```bash
make back
```

Start only the frontend:

```bash
make front
```

Run the Django server manually:

```bash
make runserver
```

Create a superuser:

```bash
make createsuperuser
```
---

## Stopping & Cleaning Up

```bash
make down
```

This will stop all containers and delete local database volume data.


---

## Database Migrations

Create and apply migrations:

```bash
make makemigrations
make migrate
```

If you need to create an empty migration for an app (e.g. `common`):

```bash
make makemigrations-common
```

---


## File conventions (backend)

- `urls.py` – route definitions
- `views.py` – controller layer (handles request and response)
- `models.py` – ORM schema (database layer)
- `services.py` – business logic (calls models and other logic)



