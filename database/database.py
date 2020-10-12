import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///' + os.path.join(basedir, 'data.sqlite'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Employee(db.Model):
    _tablename__ = 'employee' #table names

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.Text)

    emailId = db.Column(db.Text)

    publicKey=db.Column(db.Text)
    #one to many relationship
    member = db.relationship('MemberOf',backref='emp',cascade="all,delete",lazy='dynamic')


    def __init__(self,name,emailId,publicKey):
        self.name = name
        self.emailId=emailId
        self.publicKey = publicKey

    def __repr__(self):
        # This is the string representation of a puppy in the model
        return f" {self.name} 's emailId is {self.emailId} ."


class Group(db.Model):
    __tablename__='Groups'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text,unique=True)
    createdOn=db.Column(db.Date)
    admin=db.Column(db.Text)
    memberCount=db.Column(db.Integer,unique=True)
    memberOf = db.relationship('MemberOf',backref='grp',cascade="all,delete",lazy='dynamic')


    def __init__(self,name,adminName,count):
        self.name=name
        self.createdOn=date.today()
        self.admin=adminName
        self.memberCount=count

    def __repr__(self):
        return f"{self.name} is a group with Id {self.id}.It was created on {self.createdOn} by {self.admin}."



class MemberOf(db.Model):
    __tablename__="member_of"
    empId=db.Column(db.Integer,db.ForeignKey('employee.id'),primary_key=True)
    grpId=db.Column(db.Integer,db.ForeignKey('Groups.id'),primary_key=True)

    def __init__(self,membId,grpId):
        self.empId=membId
        self.grpId=grpId

    def __repr__(self):
        all_puppies = Group.query.all()
        return f"{self.empId} is a member of {self.grpId}"
