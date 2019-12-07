#### CUS1166 Project Group B.
This project is a basic web application utlizing:
Python
Flask
SQLAlchemy
HTML
Google maps API
#### It's Purpose:
To learn the microframework 'Flask'
The application allows users to add vehicles to their 'fleet'
It allows users to track their mileage for oil changes and updating it within the database
It allows users to book appointments with mechanics to schedule maintenance
It provides reminders through emailing users 3 days before they have an appointment coming up
It tracks inspections for vehicles from the last time you had an inspection

#### Basic folder structure.
- `models.py` : includes database models.
- `app.py`: Is the main file that starts your project.
- `migrate`: Provides version control of the DB throughout the project.
- `app.db` : Is the main database in the project.
- `forms.py` : includes the file for forms through the web application.
- `routes.py`: includes the logic throughout the project
#### CUS1166 Flask application.

Once the project is cloned, all dependencies are met and you have a virtual environment setup

Type in:

```shell
flask db init
flask db migrate
flask db upgrade
```
This will provide you with a clean DB on your machine.

Then, type in:
```shell
flask run
```
