from threading import Thread, Event
from app.routes import notificationEmail, appNotification

class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(86400): #86400 = 60*60*24 = secondes in 1 day
            notificationEmail()
            appNotification()

def main():
    stopFlag = Event()
    thread = MyThread(stopFlag)
    thread.start()

main()
