from app import app, db
from app.models import User, Car, Availability, Schedules


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car, 'Availability': Availability, 'Schedules': Schedules}
