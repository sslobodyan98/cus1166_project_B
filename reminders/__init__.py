#from flask import Flask
#from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from flask_bootstrap import Bootstrap

#from sqlalchemy import event
#from .tasks import on_reminder_save

#def create_app(object_name):
#    app = Flask(__name__)
#    app.config.from_object(object_name)

#    db.init_app(app)
#    event.listen(Reminder, 'after_insert', on_reminder_save)
#    â€¦
from flask import Flask

app = Flask(__name__)
