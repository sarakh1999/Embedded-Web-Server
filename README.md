# Embedded Web Server

## Team members:

Ghazal Shenavar 97101897

Sara Khosravi 97101586

Sepehr Safari 97108263

## List of contents
- [Setup Project](#setup-project)
- [Build database](#build-database)
- [Update database](#update-database)
- [How to use](#how-to-use)

## Setup project

1. Go into the project dir:

```
cd raspberry_webserver
```

2. Create a virtual environment:

```
python -m venv venv
```

3. Activate the venv:

```
source venv/bin/activate
```

4. Install requirements:

```
pip install -r requirements.txt
```

5. Build database. You can see the details in [Build database section](#build-database)

6. Make migrations:

```
python manage.py makemigrations
```

7. Migrate:

```
python manage.py migrate
```

8. Create a super user (i.e. an admin):

```
python manage.py createsuperuser
```

## Build database

1. install Mysql.

2. Create the user.

```
sudo mysql
> CREATE USER 'rasp_user'@'localhost' IDENTIFIED BY 'rasp_user';
> GRANT ALL PRIVILEGES ON * . * TO 'rasp_user'@'localhost';
> FLUSH PRIVILEGES;
> exit
```

3. Create the database.
```
mysql -u rasp_user -p
> CREATE DATABASE `rasp_db` CHARACTER SET utf8;
> exit
```

- The specifications of user and database are according to what we've set in [settings.py](./raspberry_webserver/core/settings.py). They are specified in `DATABASES` variable.

## Update database

1. Make migrations:

```
python manage.py makemigrations
```

2. Migrate:

```
python manage.py migrate
```

## Run server

Run server:

```
python manage.py runserver 0.0.0.0:8000
```

- Remember to activate and deactivate the server. The commands used are respectively `source venv/bin/activate` and `deactivate`.

## How to use

The server will be run on `127.0.0.1:8000`

### Basic routes

`/register`: Signup.

`/login`: Login.

`/panel`: Go to root directory.

`/admin`: Admin panel. Remember to create an admin with `python manage.py createsuperuser` command first.
