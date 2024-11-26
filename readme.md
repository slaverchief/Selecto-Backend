## Meta-info

This is a backend for an application that implements sampling using the algorithm of the hierarchy analysis method invented by Thomas Saati. The backend is implemented according to the REST principle.

**STACK**: **`Django REST Framework`**, **`PostgreSQL`**

## Installation

- Clone repository, using: `git clone https://github.com/slaverchief/Selecto.git`

- Create a virtualenv and install all requirements, using `pip install -r requirements.txt` (you should activate environment before)

- Set the all required environment variables:
	- **SECRET_KEY** - The secret key in setting.py file
	- **DEBUG** - The value that sets the status of the DEBUG variable(1 or 0)
	- **MAIN_HOST** - The address of the host on which the backend will run
	- **DB_NAME** - Name of app's database
	- **DB_USERNAME** - User for app's database
	- **DB_PASSWORD** - Password for user of app's database
	- **DB_HOST** - IP address of the server with your database

- Set up the project for your database in settings.py. In my case PostgreSQL was chosen, you can do the way you want

- Make migrations, using: `python manage.py makemigrations`

- Run `python manage.py migrate`

- Run the server, using `python manage.py runserver`.

## Documentation

In process...

