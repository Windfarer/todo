from todo import app,mail
from todo.models import User
from threading import Thread
from flask.ext.mail import Message
from config import MAILADMIN

def send_async_email(msg):
    with app.app_context():
         mail.send(msg)
    
 
# def sendmail(userlist):
#
#     for user in userlist:
#         usermail=User.objects(username=user)
#         msg = Message('test subject', sender = ADMIN, recipients = usermail)
#         msg.html = mailtext
#         thr = threading.Thread(target = send_async_email, args = [msg])
#         thr.start()
        
def mailsender(text,recipients):

    msg = Message('test subject', sender = MAILADMIN, recipients = recipients)
    msg.html = text
    thr = Thread(target = send_async_email, args = [msg])
    thr.start()