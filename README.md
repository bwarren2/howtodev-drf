# Readme

## TLDR

Bring it up with `docker-compose up`

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
