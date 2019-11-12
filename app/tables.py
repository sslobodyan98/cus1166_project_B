from flask_table import Table, Col


class Schedules(Table):
    id = Col('Id', show=False)
    user = Col('User')
    mechanic = Col('Mechanic')
    appointment_date = Col('Appointment Date')
    appointment_time = Col('Appointment Time')
