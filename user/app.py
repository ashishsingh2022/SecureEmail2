
import os
from flask import Flask,request
from forms import  *
from flask import Flask, render_template, url_for, redirect,flash
import requests
import json
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
domain_name= "http://127.0.0.1:5000"

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
    form = Subject_and_Body()
    if form.validate_on_submit():
        subject = form.subject.data
        body=form.body.data
        print(subject)
        print("\n\n\n")
        print(body)
        return render_template('body_and_subject.html',form=form)
    return render_template('body_and_subject.html',form=form)

@app.route('/add_attachments',methods=['POST','GET'])
def add_attachments():
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
                return("  Summary ")
    return render_template('select_files.html',form=form,files=files)




if __name__ == '__main__':
    app.run(host="localhost", port=8002, debug=True)
