# Howtodev DRF

Work through a series of tests setting up example DRF APIs, culminating in browsable, automatic Redoc-documentation and an interactive API dashboard.

The tests:

![Guidebook](howtodev-server/img/guidebook.png)

The Redocs:

![Redocs](howtodev-server/img/redocs.png)

The API dash:

![Swagger](howtodev-server/img/swagger.png)

## Setup TLDR

Bring it up with `docker-compose up`

Vue is served on `http://localhost:8001/`

Django is served on `http://localhost:8080/`, with the API root at `http://localhost:8080/api/`.

If you want to use the vue UI, swap the commented/uncommented commands in `howtodev-vue` in `docker-compose.yml`.

### Database setup

Bring it up, then

`docker exec -it howtodev-database bash`

To get into a container, and

`psql -U postgres`

to get a postgres shell.

Create the DB:
`createdb -U postgres howtodev`

Create the user:
`create user howtodev with superuser;`
`alter user howtodev with password 'abadpass';`

Close out, and go into the server:
`docker exec -it howtodev-server bash`

Migrate the DB:
`python howtodev/manage.py migrate`

See if it runs at `http://127.0.0.1:8001/`!

### Optional setup

Create a superuser if you want one:
`python howtodev/manage.py createsuperuser` within the server

## Tests

Run with `pytest`
