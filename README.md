#### CUS1166 Project Group B.

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
