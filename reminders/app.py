from flask import Flask
from flask_mail import Mail, Message
import smtplib

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
#app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'mariyamelshrieff@gmail.com'
app.config['MAIL_PASSWORD']= 'AD22703259me'
app.config['MAIL_DEFAULT_SENDER'] = 'mariyamelshrieff@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
#app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTATCHMENTS'] = False

from app.views import app
app.run(debug=True)

mail = Mail (app)
#Specifying the recipents



@app.route ('/')
def index():
    msg = Message('Oil Change Reminder Notification', recipients=['goped35282@hideemail.net'])
    msg.body = ' Hi, Its time for you to schedule your next car maintenance appointment as your oil needs to be changed!'
    msg.html = '<b>This is a Reminder Notification </b>'
    mail.send(msg)

    return ('Reminder sent')
#need a list of user with their email
@app.route ('/bulk')
def bulk():
        users = [{'name' : 'Anthony', 'Email ': 'email@email.com'},
                {'Alice', 'Alice@example.com'},
                {'Sam', 'Sam@example.com'},
                {'Mike', 'Mike@example.com'}]
        #flask connection ( listing the group of users I have)
        #Back to max emails | email put the list of users or make it read from the database
        msg = Message('Notification Reminder', recipients = [users ['email']])
        msg.body= 'Hey There! this is a reminder of your upcoming notification'
        conn.send(msg)


if __name__ == '__main__':
    app.run()
