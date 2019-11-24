from app import app, db
from app.models import User, Car, Availability, Schedules, Reviews, Mechanic_Ratings


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car, 'Availability': Availability, 'Schedules': Schedules,
            'Reviews': Reviews, 'Mechanic_Ratings': Mechanic_Ratings}
