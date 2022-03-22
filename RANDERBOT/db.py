from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bumps.db'
db = SQLAlchemy(app)

class User(db.Model):
    pkey = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer,unique=True)
    username = db.Column(db.String(80),   unique=True, nullable=False)
    serverid = db.Column(db.Integer, nullable=False)

def add_ping(serveride,ide,name):
  user = User(id=ide,username=name,serverid=serveride)
  db.session.add(user)
  db.session.commit()

def ping_check():
  userslist = []
  users = User.query.all()
  for user in users:
    userslist.append(user.id)
  return userslist

def remove_ping(ide):
  User.query.filter_by(id=ide).delete()
  db.session.commit()
def users_check(serveride):
  userslist = []
  users = User.query.filter((User.serverid == serveride))
  for user in users:
    userslist.append(user.username)
  return userslist