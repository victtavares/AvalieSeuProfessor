from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index')
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
    if lform.validate_on_submit():
        return redirect('/index')
    
    return render_template('login.html', 
                           title='Sign In',
                           rform = rform,
                           lform=lform)


@app.route('/register', methods=['POST'])
def register():
    rForm = RegisterForm()
    lform = LoginForm()
    if rForm.validate_on_submit():
        return redirect('/index')
    
    return render_template('login.html', 
                           title='Sign In',
                           rform=rForm,
                           lform=lform)