
import os
from flask import Flask,request
from forms import  *
from flask import Flask, render_template, url_for, redirect,flash
import requests
import json
from werkzeug.utils import secure_filename
from packages.huffman import *
from package.encryption import *
from package.decryption import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
domain_name= "http://127.0.0.1:8001"

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

emails=[]
subject=""
body=""
files=[]

@app.route('/select_receiver',methods=['POST','GET'])
def select_receiver():
    global emails,subject,body,files
    address='/queryAll'
    link=domain_name+address
    code,data=get_request(link)
    employees=data['reply']
    if request.method=='POST':
        emails=request.form.getlist('say_hello')
        return redirect(url_for('add_Email'))
    return render_template('receiver_list.html',employees=employees)

@app.route('/create_an_email', methods=['POST','GET'])
def add_Email():
    global emails,subject,body,files
    form = Subject_and_Body()
    if form.validate_on_submit():
        subject = form.subject.data
        body=form.body.data
        return redirect(url_for("add_attachments"))
    return render_template('body_and_subject.html',form=form)

@app.route('/add_attachments',methods=['POST','GET'])
def add_attachments():
    global emails,subject,body,files
    form=Files()
    if form.validate_on_submit():
        if form.deleteAll.data:
            files.clear()
            return render_template('select_files.html',form=form,files=files)
        else:
            if form.file.data.filename != '':
                filename = secure_filename(form.file.data.filename)
                form.file.data.save('uploads/'+filename)
                files.append(str(filename))
                return render_template('select_files.html',form=form,files=files)
            else:
                return redirect(url_for('overview'))
    return render_template('select_files.html',form=form,files=files)


























@app.route('/overview',methods=['POST','GET'])
def overview():
    global emails,subject,body,files
    print(emails)
    form=sendingForm()
    if form.send.data:
        #Compress
        body=compress_text(file_name="",string=body)
        
        #body=encrypt()
        for file in files:
            compress_text(file_name=file,string="")
            #encrypt()
        #encrypt
        return(body)
    else:
        pass
    return render_template('overview.html',emails=", ".join(emails),subject=subject,body=body,files=files,form=form)



if __name__ == '__main__':
    app.run(host="localhost", port=8003, debug=True)
