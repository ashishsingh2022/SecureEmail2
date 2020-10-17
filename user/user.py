import os
from flask import Flask,request
from forms import  *
from flask import Flask, render_template, url_for, redirect,flash
import requests
import json
from werkzeug.utils import secure_filename
from packages.huffman import *
from packages.encryption import *
#from packages.decryption import *
from packages.email_send import *
#from packages.email_receive import *
import shutil
import getmac



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
domain_name= "http://127.0.0.1:8001"

emails=[]
empIds=[]
subject=""
body=""
files=[]



private_folder="private/"
myName="Ashish"
myEmail="as0312059@gmail.com"
myPassword="Hrscv11984@1234"
upload='uploads/'

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



@app.route('/select_receiver',methods=['POST','GET'])
def select_receiver():
    global emails,subject,body,files,empIds
    address='/queryAll'
    link=domain_name+address
    code,data=get_request(link)
    employees=data['reply']
    if request.method=='POST':
        empIds=request.form.getlist('say_hello')
        for empId in empIds:
            for employee in employees:
                if str(employee['empId'])==empId:
                    emails.append(employee['email'])
        print(emails)
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
                form.file.data.save(upload+filename)
                files.append(str(filename))
                return render_template('select_files.html',form=form,files=files)
            else:
                return redirect(url_for('overview'))
    return render_template('select_files.html',form=form,files=files)



def getAbsolutePathsOfFilesIn(dir):
    file_paths = []
    for folder, subs, files in os.walk(dir):
      for filename in files:
        file_paths.append(os.path.abspath(os.path.join(folder, filename)))
    return file_paths

def getFilesIn(dir):
     arr = os.listdir(dir)
     print("Files In temp")
     print(arr)
     return arr

def copy_files():
    uploads=getAbsolutePathsOfFilesIn('uploads')
    dest_dir =  "temp/"
    for file in uploads:
        shutil.copy(file,dest_dir)



@app.route('/overview',methods=['POST','GET'])
def overview():
    global emails,subject,body,files
    form=sendingForm()
    if form.send.data:
        body=compress_text(file_name="",string=body)
        senderPrivateKey=private_folder+myName+"_keyPair.pem"
        myPassphrase=getmac.get_mac_address()
        for file in files:
            compress_text(file_name=file,string="")
        for empId in empIds:
            copy_files()
            address="/email_and_key/"+empId
            link=domain_name+address
            res=get_request(link)
            jsonDict=res[1]
            email_key_list=jsonDict['reply']
            email=email_key_list[0]
            receiverPublicKey= email_key_list[1]
            temp_files=getFilesIn('temp')
            for file in temp_files:
                encipher(senderPrivateKey,receiverPublicKey,myPassphrase,file,"")
            encryptedFiles= getAbsolutePathsOfFilesIn('temp')
            send_email(EMAIL_ADDRESS=myEmail,EMAIL_PASSWORD=myPassword,contacts=emails,subject=subject,body=body,files=encryptedFiles)
            for file in encryptedFiles:
                os.remove(file)
        files=getAbsolutePathsOfFilesIn(upload)
        for file in files:
            os.remove(file)
        emails.clear()
        empIds.clear()
        subject=""
        body=""
        files.clear()
        return "Mail Sent"
    elif form.cancel.data:
        emails.clear()
        empIds.clear()
        subject=""
        body=""
        for file in files:
            os.remove(upload+file)
        files.clear()
    return render_template('overview.html',emails=", ".join(emails),subject=subject,body=body,files=files,form=form)



if __name__ == '__main__':
    app.run(host="localhost", port=8003, debug=True)
