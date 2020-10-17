from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from database import *
import requests
api = Api(app)

# Operations On Employee
def insert_employee(name,email,pubKey):
    person = Employee.query.filter_by(name=name).filter_by(emailId=email).first()
    if person!=None:
        return False," The Employee Is Already Registered ."
    new_emp=Employee(name,email,pubKey)
    db.session.add(new_emp)
    db.session.commit()
    person = Employee.query.filter_by(name=name).filter_by(emailId=email).filter_by(publicKey=pubKey).first()
    id=person.id
    print("1 Row Inserted")
    return True,f" The Employee Got Registered with Employee Id {id}."

def email_key(empId):
    person = Employee.query.filter_by(id=empId).first()
    if person==None:
        return False,"No Employee with this employee Id exists."
    data=[]
    data.append(person.emailId)
    data.append(person.publicKey)
    return True,data

#Operations On Groups and Members Of
def createGroup(name,admin,members):
    if len(members)==0:
        return False,"Atleaset One Member Required in Group"
    e=Employee.query.filter_by(id=admin).first()
    admin_name=e.name
    new_grp=Group(name,admin_name,len(members))
    db.session.add(new_grp)
    createdGrp=Group.query.filter_by(name=name).first()
    createdId=createdGrp.id
    members=list(set(members))
    for empId in members:
        new_grp=MemberOf(empId,createdId)
        db.session.add(new_grp)
    db.session.commit()
    return True,"Success!! Group Created."

def viewGroup(name_):
    Grp=Group.query.filter_by(name=name_).first()
    if Grp==None:
        return False,"Sorry!! No Such Group Exists."
    id=Grp.id
    members=MemberOf.query.filter_by(grpId=id).all()
    members_of_grp="\nThe Members Of The Group Are\n"

    for emp in members:
        e=Employee.query.filter_by(id=emp.empId).first()
        name=e.name
        #print(name)
        members_of_grp=members_of_grp+name+"\n"
    groupDetails=Grp
    return True,str(Grp)+members_of_grp,members

def deleteEmpId(empId):
    emp = Employee.query.get(empId)
    if emp==None:
        return False,"No Employee with the requested EmployeeId exists in the database,or you already deleted the employee with requested EmployeeId."
    db.session.delete(emp)
    grps=MemberOf.query.filter_by(empId=empId).all()
    for grp in grps:
        grpId=gpr.id
        delMembership=MemberOf.query.filter_by(empId=empId).filter_by(grpId=grpId)
        db.session.delete(delMembership)
        decGrp= Group.query.get(grpId)
        decGrp.count=decGrp-1;
        if decGrp.count==0:
            db.session.delete(decGrp)
        else:
            db.session.add(decGrp)
    db.session.commit()
    return True,f"Employee with EmployeeId {empId} got deleted"

def deleteAll():
    emp = Employee.query.all()
    print(emp)
    if emp==[]:
        return False,"No Employee Record to be deleted ."
    db.session.query(Employee).delete()
    db.session.query(MemberOf).delete()
    db.session.query(Group).delete()
    db.session.commit()
    return True,"All employees record got deleted"

def returnAll():
    employees = db.session.query(Employee)
    emp_list=[]
    if employees==None:
        return False,"No Employee Registered"
    #names = db.session.query(Employee.name).all()
    ##pubKeys = db.session.query(Employee.publicKey).all()
    for emp in employees:
        curr_emp={'empId':emp.id,'name':emp.name,'email':emp.emailId}
        emp_list.append(curr_emp)
    return True,emp_list#,names,empIds,pubKeys





############################################## APIS


class Insert(Resource):
    def post(self,name,email,dbaPass):
        pubKey=request.get_json()['Key']
        response=insert_employee(name,email,pubKey)
        message={'status':response[0],'reply':response[1]}
        return message, 200

class Query(Resource):
    def get(self,empId):
        response=email_key(empId)
        message={'status':response[0],'reply':response[1]}
        return message


class AllEmployee(Resource):
    def get(self):
        response=returnAll()
        return {'status':response[0],'reply':response[1]}

group_name=""
group_admin=0
group_members=[]
class CreateGroup(Resource):
    def post(self,name,admin):
        global group_name
        global group_admin
        global group_members
        adminExists=Employee.query.filter_by(id=admin).first()
        if adminExists==None:
            return {'status':'False','reply':"You are not a registered employee. So You are not permitted to create the group"}
        groupExists=Group.query.filter_by(name=name).first()
        if groupExists==True:
            return {'status':'False','reply':"A group with requested name already exists"}
        group_name=name
        group_admin=admin
        group_members.append(admin)
        message={'status':'True','reply':"You Can Create the Group"}
        return message
class AddMembers(Resource):
    def post(self,empId):
        global group_name
        global group_admin
        global group_member
        print(group_members)
        print(group_name+" h "+str(group_admin))
        empExists=Employee.query.filter_by(id=empId).first()
        if empExists==None:
            return {'status':False,'reply':f"Employee Id {empId} is not a Valid Employee Id.Please Verify"}
        group_members.append(empId)
        return {'status':True,'reply':" Valid Employee Id "}
class Create(Resource):
    def post(t=True):
        global group_name
        global group_admin
        global group_member
        response=createGroup(group_name,group_admin,group_members)
        group_members.clear()
        group_name=""
        group_admin=0
        message={'status':response[0],'reply':response[1]}
        return message

class DeleteEmpId(Resource):
    def post(self,empId):
        response=deleteEmpId(empId)
        message={'status':response[0],'reply':response[1]}
        return message

class Delete(Resource):
    def get(self):
        response=deleteAll()
        message={'status':response[0],'reply':response[1]}
        print(message)
        return message

class View(Resource):
    def get(self,groupName):
        print(groupName)
        response=viewGroup(groupName)
        message={'status':response[0],'reply':response[1]}
        if response[0]:
            members=[]
            for m in response[2]:
                members.append(m.empId)
            message['members_ids']=members
        return message

api.add_resource(Insert, '/insert/<string:name>/<string:email>/<string:dbaPass>')
api.add_resource(Query, '/email_and_key/<int:empId>')
api.add_resource(CreateGroup, '/CreateGroup/<string:name>/<int:admin>')
api.add_resource(AddMembers, '/AddMembers/<int:empId>')
api.add_resource(Create, '/Submit')
api.add_resource(View, '/viewgroup/<string:groupName>')
api.add_resource(DeleteEmpId, '/Delete/<int:empId>')
api.add_resource(Delete, '/Delete')
api.add_resource(AllEmployee,'/queryAll')


@app.route('/')
def index():
    return "<h1>The Database is Running </h1>"

if __name__ == '__main__':
    db.create_all()
    app.run(host="localhost",port=8001,debug=True)
