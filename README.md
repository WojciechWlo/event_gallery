# event_gallery

# Environment
Create two files in project folder:
* .env.dev
```
APP_ENV=development
DEBUG=True

DATABASE_URL=sqlite:///./db.sqlite3

SERVER_URL=http://localhost:8000

SSL_KEYFILE=/certs/server.key
SSL_CERTFILE=/certs/server.cert
```
* .env.prod
```
APP_ENV=production
DEBUG=False

SERVER_URL=https://localhost:8000

SSL_KEYFILE=/certs/server.key
SSL_CERTFILE=/certs/server.cert

POSTGRES_USER=admin
POSTGRES_PASSWORD=securepassword123
POSTGRES_DB=pgdb
DATABASE_URL=postgresql+psycopg2://admin:securepassword123@db:5432/pgdb
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

## Create app user
In fastapi service console generate hashed password using command:
```
python gen_hash_phrase.py
```
When creating new user, use generated hash as password!

## Dev mode
* Go to http://localhost:8081/ and on the left side choose "users" table.
* Choose Insert.
* Insert "user" name and "hashed_password" generated by "gen_hash_phrase.py".
* Click "Insert" button.

## Prod mode
* Go to http://localhost:5050/ and log in using "Email Address" and "Username" used in pgadmin service ([PGADMIN_DEFAULT_EMAIL], [PGADMIN_DEFAULT_PASSWORD]).
* Connect to server using:
    * Server Name - postgres service container_name.
    * Host name/address - postgres service container_name.
    * Port - 5432
    * Database - [POSTGRES_DB]
    * User - [POSTGRES_USER]
    * Password - [POSTGRESS_PASSWORD]
* In Query console insert:
```
insert into users (name, hashed_password) values ("user_name", "hashed_password");
```
* Click "Execute Script" Button.

## Changing passwords and variables
After building environments, you should remember about changing any passwords defined in files .env and .yaml.

### Changing password in PGAdmin
To change password go to http://localhost:5050/ and log in. In upper right corner click email of logged account and select "Change Password".

### Changing password in PostgreSQL
To change password, you have to connect with your database, for example through PGAdmin panel. in Query console, insert command:

```
ALTER USER user_name WITH PASSWORD "new_password";
```

