from flask import render_template, flash, redirect, request, url_for
from app import app, db
from .forms import LoginForm, RegisterForm, RegisterProfessorForm
from .models import User, Professor, Department
from flask.ext.login import login_required, logout_user, login_user, current_user
from decorators import admin_required, permission_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'nickname': 'Victor'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    rform = RegisterForm()
    print(lform.validate_on_submit)
    if request.method == 'POST' and lform.validate():

        user = User.query.filter_by(email=lform.email.data).first()
        if user is not None and user.verify_password(lform.password.data):
            login_user(user, False)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    
    return render_template('login.html', 
                           rform = rform,
                           lform = lform,
                           loginActive = "active",
                           registerActive = "")


@app.route('/register', methods=['GET','POST'])
def register():
    rForm = RegisterForm()
    lform = LoginForm()
    if rForm.validate_on_submit():
        user = User(email=rForm.email.data,
        name=rForm.name.data,
        college = rForm.college.data,
        password=rForm.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Parabens! voce esta cadastrado, pode realizar o login agora')



    return render_template('login.html', 
                           rform=rForm,
                           lform=lform,
                           loginActive = "",
                           registerActive = "active")

@app.route('/admin')
@login_required
@admin_required
def usuarios():
 return "For administrators!"

@login_required
@app.route('/addProfessor', methods=['GET','POST'])
def adicionarProfessor():
    form = RegisterProfessorForm()

    adminApproved = False
    if current_user.isAdmin:
        adminApproved = True


    if form.validate_on_submit():
        professor = Professor(name=form.name.data,
        department_id=form.department.data,
        wasAcceptedByAdmin = adminApproved)

        if professor == None:
            db.session.add(professor)
            db.session.commit()
            flash("Erro ao recomendar o professor, tente mais tarde!")
        else:
            flash("Professor recomendado com sucesso!")
        

    return render_template('adicionar_professor.html',
                            form = form)

@app.route('/logout')
@login_required
def logout():
 logout_user()
 flash('You have been logged out.')
 return redirect(url_for('login'))

