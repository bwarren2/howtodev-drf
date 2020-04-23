# Readme

## TLDR

Bring it up with `docker-compose up`

Vue is served on `http://localhost:8001/`

Django is served on `http://localhost:8080/`, with the API root at `http://localhost:8080/api/`.

If you want to use the vue UI, swap the commented/uncommented commands in `howtodev-vue` in `docker-compose.yml`.

## Database setup

Bring it up, then

`docker exec -it howtodev-database bash`

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

## Optional setup

Create a superuser if you want one:
`python howtodev/manage.py createsuperuser` within the server
