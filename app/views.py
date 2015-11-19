from flask import render_template, flash, redirect, request, url_for
from app import app, db
from .forms import LoginForm, RegisterForm, RegisterProfessorForm, BuscaForm, PostForm
from .models import User, Professor, Department, Post
from flask.ext.login import login_required, logout_user, login_user, current_user
from .decorators import admin_required, permission_required
import datetime

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

@app.route('/logout')
@login_required
def logout():
 logout_user()
 flash('You have been logged out.')
 return redirect(url_for('login'))


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





@app.route('/users')
@login_required
@admin_required
def listarUsuarios():
    users = User.query.all()
    return render_template('listar_usuarios.html',
        users = users)

@app.route('/users/delete/<id>')
@login_required
@admin_required
def removerUsuario(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("listarUsuarios"))



@app.route('/professors')
@login_required
@admin_required
def listarProfessoresPendentes():
    professors = Professor.query.filter_by(wasAcceptedByAdmin = False)
    return render_template('lista_professores.html',
        professors = professors)

@app.route('/professors/approve/<id>')
@login_required
@admin_required
def aprovarProfessor(id):
    professor = Professor.query.get(id)
    professor.wasAcceptedByAdmin = True
    db.session.commit()
    return redirect(url_for("listarProfessoresPendentes"))



 
 

@login_required
@app.route('/addProfessor', methods=['GET','POST'])
def adicionarProfessor():
    form = RegisterProfessorForm()


    if form.validate_on_submit():

        adminApproved = False
        if current_user.isAdmin():
            adminApproved = True

        professor = Professor(name=form.name.data,
        department_id=form.department.data,
        wasAcceptedByAdmin = adminApproved)

        if professor == None:
            flash("Erro ao recomendar o professor, tente mais tarde!")
        else:
            db.session.add(professor)
            db.session.commit()
            flash("Professor recomendado com sucesso!")
        

    return render_template('adicionar_professor.html',
                            form = form)


@app.route('/professores/<department>')
@login_required
def listProfessores(department):

    dept = Department.query.get(department)
    allProfessorsFromDept = Professor.query.filter_by(department_id = dept.id , wasAcceptedByAdmin = True)
    print(allProfessorsFromDept)
    return render_template("lista_professor.html",
                            dept = dept,
                            professors = allProfessorsFromDept)



@app.route('/professor/<id>',  methods=['GET','POST'])
@login_required
def detailProfessor(id):
    professor = Professor.query.get(id)

    return render_template("detail_professor.html",
                            professor = professor)

@app.route('/professor/<id>/post',  methods=['GET','POST'])
@login_required
def avaliaProfessor(id):
    pForm = PostForm()
    professor = Professor.query.get(id)
    if pForm.validate_on_submit() : 

        currentPost = Post(body = pForm.body.data,
        course = pForm.course.data,
        ratingTeaching = pForm.ratingTeaching.data,
        ratingEase = pForm.ratingEase.data,
        gradeOnCourse = pForm.gradeOnCourse.data,
        hideUser = pForm.hideUser.data,
        author = current_user,
        timestamp = datetime.datetime.utcnow(),
        about = professor)

        if currentPost == None:
            flash("Erro ao avaliar o professor, tente mais tarde!")
        else:
            db.session.add(currentPost)
            db.session.commit()
            flash("Professor avaliado com sucesso!")

    return render_template("avalia_professor.html",
                            professor = professor,
                            form = pForm)


@app.route('/post/delete/<idAvaliacao>/professor/<idProfessor>')
@login_required
@admin_required
def removerAvaliacao(idProfessor, idAvaliacao):
    post = Post.query.get(idAvaliacao)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("detailProfessor", id = idProfessor))
