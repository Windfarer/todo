from wtforms import Form, TextField, BooleanField, PasswordField, validators


class LoginForm(Form):
    username = TextField('username',[validators.Required()])
    password = PasswordField('password',[validators.Required()])
    remember_me = BooleanField('remember_me', default = False)


class RegisterForm(Form):
    username = TextField('username',[validators.Required()])
    password = PasswordField('password',[validators.Required()])
    email = TextField('email',[validators.Required(),validators.Email(message=None)])
    
    
class TaskForm(Form):
    content=TextField('Task Content',[validators.Required()])
    deadline=TextField('Deadline',[validators.Required()])
    assign=TextField('Assign')
    
class SubTaskForm(Form):
    content=TextField('Task Content',[validators.Required()])
    deadline=TextField('Deadline',[validators.Required()])