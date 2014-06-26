from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from flask.ext.mail import Mail

mail = Mail()

app = Flask(__name__)




app.config.from_object('config')

login_manager=LoginManager()
login_manager.init_app(app)

db = MongoEngine(app)
if __name__ == '__main__':
    app.run()


mail.init_app(app)

from todo import views
from todo import models
from todo import mail
