from flask import render_template, flash, redirect, request, url_for
from app import app, db
from .forms import LoginForm, RegisterForm, RegisterProfessorForm, BuscaForm
from .models import User, Professor, Department
from flask.ext.login import login_required, logout_user, login_user, current_user
from decorators import admin_required, permission_required

@app.route('/',  methods=['GET','POST'])
@app.route('/index',  methods=['GET','POST'])
@login_required
def index():
    bForm = BuscaForm()

    if bForm.validate_on_submit():
        selectedDep = bForm.department.data
        return redirect(url_for("listProfessores", department = selectedDep))

    return render_template("index.html",
                           form = bForm)


@app.route('/professores/<department>',  methods=['GET','POST'])
@login_required
def listProfessores(department):
    dept = Department.query.get(department)
    print(dept)
    return render_template("lista_professor.html",
                            dept = dept,
                            professors = dept.professors)

@app.route('/professor/<id>',  methods=['GET','POST'])
@login_required
def detailProfessor(id):
    professor = Professor.query.get(id)

    return render_template("detail_professor.html",
                            professor = professor)
    



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

