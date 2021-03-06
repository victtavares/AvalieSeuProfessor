from app import app, models, db
from flask.ext.login import current_user
import datetime
#admin User
if not models.User.query.filter_by(email="victtavares1@gmail.com").first():
  u = models.User(email='victtavares1@gmail.com', name='Victor Tavares', password='gato',college = "Universidade Federal da Bahia", role =1)
  db.session.add(u)
  db.session.commit()


if not models.User.query.filter_by(email="victtavares@gmail.com").first():
  u = models.User(email='victtavares@gmail.com', name='No Admin', password='gato',college = "Universidade Federal da Bahia", role =0)
  db.session.add(u)


if models.Department.query.count() == 0:
  d1 = models.Department(name="Departamento de Matematica")
  d2 = models.Department(name="Departamento de Quimica")
  d3 = models.Department(name="Departamento de Fisica")
  db.session.add(d1)
  db.session.add(d2)
  db.session.add(d3)


users = models.User.query.all()
for u in users:
  print(u.id,u.name, u.email, u.college, u.role)


if models.Professor.query.count() == 0:
  p1 = models.Professor(name="professor1",currentDepartment=d1)  
  p2 = models.Professor(name="professor2",currentDepartment=d1)  
  p3 = models.Professor(name="professor3",currentDepartment=d2)  
  p4 = models.Professor(name="professor4",currentDepartment=d2, wasAcceptedByAdmin = True)
  db.session.add(p1)
  db.session.add(p2)
  db.session.add(p3)
  db.session.add(p4)


  d1 = models.Post(body="Este professor e muito bom! Aulas super interresantes e com uma didatica incrivel.",
                          course = "Teoria da Computacao",
                          ratingTeaching = "9",
                          ratingEase = "9",
                          gradeOnCourse = "8",
                          timestamp = datetime.datetime.utcnow(),
                          hideUser = False,
                          author = u,
                          about = p3)

  d2 = models.Post(body="Gostei da materia! bem facil!",
                          course = "Engenharia de software",
                          ratingTeaching = "7",
                          ratingEase = "9",
                          gradeOnCourse = "6",
                          timestamp = datetime.datetime.utcnow(),
                          hideUser = False,
                          author = u,
                          about = p3)

  db.session.add(d1)
  db.session.add(d2)



db.session.commit()

posts = models.Post.query.all()
for d in posts:
  print(d.id,d.course, d.author.name, d.about.name)

professors = models.Professor.query.all()
for p in professors:
  print(p.id,p.name, p.currentDepartment.name, p.wasAcceptedByAdmin)


