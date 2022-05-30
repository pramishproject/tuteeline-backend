Student Master
==================

Quickstart
----------
Install python requirements:

::

  $ python -r requirements/local.txt


Update Env Variables:
    * Update env variables on **example.env** file, and save as **'.env'**.


Running Migrate:

::

  $ python manage migrate


Create Superuser:

::

  $ python manage createsuperuser


Run server:

::

  $ python manage runserver




Documentation
-------------
apps:
    * apps are stored in **apps/** folder

settings:
    * Django **Settings** are under **config/** folder
    * config/base.py for base settings
    * config/local.py for local development settings
    * config/production.py for production settings

requirements:
    * Python package requirements are listed under **requirements/** folder
    * requirements/base.py for base requirements
    * requirements/local.py for local development requirements
    * requirements/production.py for production requirements