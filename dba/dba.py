
import os
from flask import Flask
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect,flash
from packages.cryptolib import GenerateKeys
import requests
import json
import getmac





app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

domain_name= "http://127.0.0.1:8001"
private_key_address="C:/Users/AshishPC/Desktop/private/"

def post_request(link):
    r = requests.post(url =link)
    code=r.status_code
    data = json.loads(r.text)
    return code,data


def get_request(link):
    r = requests.get(url=link)
    code=r.status_code
    data = json.loads(r.text)
    return code,data


@app.route('/')
def index():
    return render_template('home.html')



@app.route('/add', methods=['POST','GET'])
def add_Employee():
    form = AddForm()
    message=""
    if form.validate_on_submit():
        name = form.name.data
        email=form.email.data
        pubKey= GenerateKeys(getmac.get_mac_address(),private_key_address,name).decode()
        dbPass=form.dbPass.data
        address= "/insert/"+name+"/"+email+"/"+dbPass
        link=domain_name+address
        key={"Key":pubKey}
        res=requests.post(link, json=key)
        if res.ok:
            data=res.json()
        message=data['reply']
        #form.name.data=""
        #form.email.data=""
        #form.dbPass.data=""
        #redirect(url_for('add_Employee'))
        render_template('add.html',form=form,message=message)
    return render_template('add.html',form=form,message=message)



@app.route('/list')
def list_Employee():
    address='/queryAll'
    link=domain_name+address
    code,data=get_request(link)
    employees=data['reply']
    print("\n\n\n")
    print(employees)

    return render_template('list.html', employees=employees)


@app.route('/delete', methods=['GET', 'POST'])
def del_employee():
    form = DelForm()
    message=""
    if form.validate_on_submit():
        if form.deleteOne.data:
            id = form.id.data
            address="/Delete/"+str(id)
            link=domain_name+address
            code,result=post_request(link)
            message=result['reply']
        else:
            link=domain_name+'/Delete'
            code,result=get_request(link)
            message=result['reply']
            print(message)
        return render_template('delete.html',form=form,message=message)
    return render_template('delete.html',form=form,message=message)


if __name__ == '__main__':
    app.run(host="localhost", port=8002, debug=True)
