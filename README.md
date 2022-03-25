# codedady-backend

Repository for codedady



Install PostgreSQL::

	$ apt-get install postgresql postgresql-contrib
	$ sudo -u postgres psql
	ALTER USER postgres WITH PASSWORD 'xxx';
	create database codedady;
	\q

## Migrate and Populate Database

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ cp .env.sample .env # update it
    $ ./manage.py makemigrations
    $ ./manage.py migrate
	