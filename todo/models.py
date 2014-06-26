from todo import app, login_manager ,db
from bson import ObjectId
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import login_user, logout_user, current_user, login_required

bcrypt=Bcrypt()


class User(db.Document):
    
    username=db.StringField(required=True,unique=True)
    password=db.StringField(required=True)
    email=db.EmailField(required=True,unique=True)
    
    def __unicode__(self):
        return self.username
        

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.username)

    def is_anonymous(self):
        return True

    def get(self,username):
        return unicode(self.username)



class Task(db.Document):
    content=db.StringField(required=True)
    deadline=db.DateTimeField(required=True)
    assignlist=db.ListField(db.EmbeddedDocumentField('AssignList'))
    status=db.BooleanField(default=False)
    subtasks = db.ListField(db.EmbeddedDocumentField('SubTask'))
    endtime=db.DateTimeField()
    def __unicode__(self):
        return self.content

        
class SubTask(db.EmbeddedDocument):
    content=db.StringField(required=True)
    deadline=db.StringField(required=True)
    endtime=db.DateTimeField()
    status=db.BooleanField(default=False)
    
class AssignList(db.EmbeddedDocument):
    user=db.StringField(required=True)
