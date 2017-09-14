# server

To run the server:
	python manage.py runserver

If you are adding a new model, run these commands to migrate the model to the database:
	python manage.py makemigrations # Creates the migration
	python manage.py migrate # Applies migrations to database

To run tests:
	python manage.py test