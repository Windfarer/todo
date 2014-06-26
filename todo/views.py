from todo import app, login_manager

from flask import Flask, render_template, flash, redirect, g, request
from forms import LoginForm, RegisterForm, TaskForm, SubTaskForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from bson import ObjectId
from flask.ext.bcrypt import Bcrypt
from todo.models import User, Task, SubTask, AssignList
from todo.mail import mailsender
import re

from datetime import datetime

bcrypt=Bcrypt()

@login_manager.user_loader
def load_user(username):
    return User.objects(username=username).first()
    
    
@app.before_request
def before_request():
    g.user = current_user
    

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/')

#======user
@app.route('/',methods=['POST','GET'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    return render_template('welcome.html')

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user=User.objects(username=form.username.data).first()
        if not user:
            flash('invalid user name.')
            return render_template('login.html',
                form=form)
        if bcrypt.check_password_hash(user.password,form.password.data):
           login_user(user)
           return redirect('/task/pending')
    return render_template('login.html',
        form=form)


@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('Logout success')
    return redirect('/')
    

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        if re.match("^[0-9a-zA-Z_]+$",form.username.data):
            user = User(username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data),
            email=form.email.data)
            user.save()
            flash('Registration Successful, login please.')
            return redirect('/login')
        else: 
            flash('error username')
    return render_template('register.html', form=form)


#========show


 
@app.route('/task',methods=['GET'])
@app.route('/task/all',methods=['GET'])
@login_required
def show_task():
    tasks=Task.objects.all()
    for task in tasks:
        task.subtasks=enumerate(task.subtasks)
    return render_template('show_all.html',tasks=tasks,title='All Tasks')
    
@app.route('/task/pending',methods=['GET'])
@login_required
def show_pending():
    tasks=Task.objects(status=False)
    for task in tasks:
        task.subtasks=enumerate(task.subtasks)
    return render_template('show_pending.html',tasks=tasks,title='Pending Tasks')
    
@app.route('/task/finished',methods=['GET'])
@login_required
def show_finished():
    tasks=Task.objects(status=True)
    for task in tasks:
        task.subtasks=enumerate(task.subtasks)
    return render_template('show_finished.html',tasks=tasks,title='Finished Tasks')

    
@app.route('/task/timeout',methods=['GET'])
@login_required
def show_timeout():
    tasks=Task.objects(deadline__lte=datetime.now(),status=False)
    for task in tasks:
        task.subtasks=enumerate(task.subtasks)
    return render_template('show_timeout.html',tasks=tasks,title='Timeout Tasks',timeout=True)
    
    
    
    
    
    
#========task



@app.route('/task/add',methods=['POST','GET'])
@login_required
def add_task():
    form = TaskForm(request.form)
    nowdate=datetime.now()
    if request.method == 'POST' and form.validate():
          task = Task(form.content.data,form.deadline.data)
          if not form.assign.data:
             assignlist = AssignList(user=g.user.username)
             task.assignlist.append(assignlist)
          else:
             for user in form.assign.data.split():
                 assignlist = AssignList(user=user)
                 task.assignlist.append(assignlist)
          task.save()
          return redirect('/task/pending')
    return render_template('add.html', form=form,nowdate=nowdate)
    
    
    
@app.route('/task/edit/<task_id>',methods=['POST','GET'])
@login_required
def edit_task(task_id):
    form=TaskForm(request.form)
    task=Task.objects(id=ObjectId(task_id)).first()
    namelist=[]
    for i in task.assignlist:
        namelist.append(i.user)
    namelist=" ".join(namelist)
    if request.method == 'POST' and form.validate():
        task.content=form.content.data
        task.deadline=form.deadline.data
        task.assignlist=[]
        recipients=[]
        if not form.assign.data:
           task.assignlist.append(AssignList(user=g.user.username))
        else:
           for user in form.assign.data.split():
               if User.objects(username=user):
                   assign = AssignList(user=user)
                   task.assignlist.append(assign)
        task.save()
        
        return redirect('/task/pending')
    return render_template('edit.html', form=form, task=task,task_id=task_id,namelist=namelist)
    


@app.route('/task/delete/<task_id>',methods=['GET'])
@login_required
def delete_task(task_id):
    Task.objects(id=ObjectId(task_id)).first().delete()
    return redirect('/task/pending')
    

    
@app.route('/task/close/<task_id>',methods=['GET'])
@login_required
def close_task(task_id):
    task=Task.objects(id=ObjectId(task_id)).first()
    task.endtime=datetime.now()
    task.status=True
    task.save()
    return redirect('/task/pending')
    

    
#==========subtask

@app.route('/task/addsub/<task_id>',methods=['POST','GET'])  
@login_required  
def add_subtask(task_id):
    nowdate=datetime.now()
    form=SubTaskForm(request.form)    
    task=Task.objects(id=ObjectId(task_id)).first()
    if request.method == 'POST' and form.validate():
        subtask = SubTask()
        form.populate_obj(subtask)
        subtask.id = ObjectId()
        task.subtasks.append(subtask)        
        task.save()
        return redirect('/task/pending')
    return render_template('add_sub.html', form=form , task_id=task_id, nowdate=nowdate)
    
    
@app.route('/task/edit/<task_id>/<int:subtask_id>',methods=['POST','GET'])
@login_required
def edit_subtask(task_id,subtask_id):
    form=SubTaskForm(request.form)
    task=Task.objects(id=ObjectId(task_id)).first()
    subtask=task.subtasks[subtask_id]
    if request.method == 'POST' and form.validate():
        form=SubTaskForm(request.form)    
        task.subtasks[subtask_id].content=form.content.data
        task.subtasks[subtask_id].deadline=form.deadline.data
        task.save()
        return redirect('/task/pending')
    return render_template('edit_sub.html', form=form, subtask=subtask,task_id=task_id,subtask_id=subtask_id)


@app.route('/task/delete/<task_id>/<int:subtask_id>',methods=['GET'])
@login_required
def delete_subtask(task_id,subtask_id):
    form=SubTaskForm(request.form)    
    task=Task.objects(id=ObjectId(task_id)).first()
    del task.subtasks[subtask_id]
    task.save()
    return redirect('/task/pending')
    
    
@app.route('/task/close/<task_id>/<int:subtask_id>',methods=['GET'])
@login_required
def close_subtask(task_id,subtask_id):
    form=SubTaskForm(request.form)    
    task=Task.objects(id=ObjectId(task_id)).first()
    task.subtasks[subtask_id].status=True
    task.subtasks[subtask_id].endtime=datetime.now().date()
    task.save()
    return redirect('/task/pending')
    