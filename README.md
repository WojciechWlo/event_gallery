# event_gallery
Application to share photos and videos from given event (for example: party, concert, wedding, etc.) with organizer and guests. Uploaded media can be stored and downloaded.

![screenshot 1](docs/screen1.png)
![screenshot 2](docs/screen2.png)

# Environment
Create two files in project folder:
* .env.dev
```
APP_ENV=development
DEBUG=True

DATABASE_URL=sqlite:///./db.sqlite3

SERVER_URL=https://localhost:8000

SSL_KEYFILE=/certs/server.key
SSL_CERTFILE=/certs/server.cert

GUEST_LOGIN=guest
GUEST_PASSWORD=password
```
* .env.prod
```
APP_ENV=production
DEBUG=False

SERVER_URL=https://localhost:8000

SSL_KEYFILE=/certs/server.key
SSL_CERTFILE=/certs/server.cert

DATABASE_USER=admin
DATABASE_PASSWORD=securepassword123
DATABASE_DB=pgdb
DATABASE_URL=postgresql+psycopg2://admin:securepassword123@db:5432/pgdb

GUEST_LOGIN=guest
GUEST_PASSWORD=password
```

# Run Project

## Dev mode
```
docker-compose -f docker-compose.dev.yaml up --build
```

## Prod mode
```
docker-compose -f docker-compose.prod.yaml up --build
```

# Changes after setting project

## Change app user
In fastapi service console generate hashed password using command:
```
python gen_hash_phrase.py
```
When creating new user, use generated hash as password!

## Dev mode
* Go to http://localhost:8081/ and on the left side choose "users" table.
* Choose "Content".
* Click "Edit".
* Change "name" and "hashed_password" fields. Remember to use generated hash for password.
* Click "Update" button.

## Prod mode
* Go to http://localhost:5050/ and log in using [PGADMIN_EMAIL] and [PGADMIN_PASSWORD].
* Connect to server using:
    * Server Name - postgres service container_name.
    * Host name/address - postgres service container_name.
    * Port - 5432
    * Database - [DATABASE_DB]
    * User - [DATABASE_USER]
    * Password - [DATABASES_PASSWORD]
* In Query console insert:
```
UPDATE users
SET name = 'new_user_name', 
    hashed_password = 'new_hashed_password'
WHERE name = [GUEST_LOGIN];
```
* Click "Execute Script" Button.

## Changing passwords and variables
After building environments, you should remember about changing any passwords defined in files .env and .yaml.

### Changing password in PGAdmin
To change password go to http://localhost:5050/ and log in. In upper right corner click email of logged account and select "Change Password".

### Changing passwords in PostgreSQL
To change admin password, you have to connect with your database, for example through PGAdmin panel. In Query console, insert command:

```
ALTER USER [POSTGRES_USER] WITH PASSWORD 'new_admin_password';
```

In initdb.sql, there is created tech user (in our case its name is "sql_event_gallery"). To change its password, in Query console, insert command:
```
ALTER USER sql_event_gallery WITH PASSWORD 'new_tech_password';
```

After changing password to tech user you should change variables in .env according to password you used.
* DATABASE_USER=sql_event_gallery
* DATABASE_PASSWORD=new_tech_password
* DATABASE_URL=postgresql+psycopg2://sql_event_gallery:new_tech_password@db:5432/pgdb

Next, close docker-compose, and relaunch it with:
```
docker-compose -f docker-compose.prod.yaml up
```
