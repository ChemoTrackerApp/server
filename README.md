# server

## Requirements
    Python 2.*

## Install virtualenv
    sudo pip install virtualenv

## Create a virtual environment
    virtualenv chemotracker

## Work on the virtual environment
    source chemotracker/bin/activate
    OR
    workon chemotracker

## Install dependencies
    pip install -r requirements.txt

## To configure watson
    python manage.py installwatson
    python manage.py buildwatson

## To run the server:
    python manage.py runserver

## If you are adding a new model, run these commands to migrate the model to the database:
    python manage.py makemigrations # Creates the migration
    python manage.py migrate # Applies migrations to database

## To run tests:
    python manage.py test   

## To end the virtual environment
    deactivate

## To run the server as a detached process
    screen
    source ~/.bash_profile
    Start the server as normal
    Press Ctrl + A or Command + A (on mac)
    Press D

## To navigate back to detached process
    screen -r

