import os
import sys
import zipfile
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature import PKCS1_v1_5

def keyReader(receiver_keyPair, file, receiver_passphrase):
    # Reading private key to decipher symmetric key used
    if file=="":
        file=download+"email.bin"
    keyPair = RSA.importKey(open(receiver_keyPair, "r").read(), passphrase=receiver_passphrase)
    keyDecipher = PKCS1_OAEP.new(keyPair)
    # Reading iv and symmetric key used during encryption
    f = open(file.split('.')[0] + ".key", "rb")
    iv = f.read(16)
    k = keyDecipher.decrypt(f.read())
    f.close()
    os.remove(file.split('.')[0] + ".key")
    return k, iv

def decipher(receiver_keyPair,receiver_passphrase,sender_pubKey,file="",string=""):  #sender_pubKey
    k,iv=keyReader(receiver_keyPair, file, receiver_passphrase)
    keyDecipher = AES.new(k, AES.MODE_CFB, iv)
    bin=string
    if file!="":
        f= open(file.split('.')[0] + ".bin", "rb")
        bin = f.read()
        f.close()
        os.remove(file.split('.')[0] + ".bin")
    s=keyDecipher.decrypt(bin)
    if sigVerification(sender_pubKey, s,file)==False:
        return False,""
    if file!="":
        f= open(file.split('.')[0]+"_decrypted.txt", "wb")
        f.write(s)
        f.close()
    return True,s.decode()


def sigVerification(sender_pubKey, s,file):
    # Generating decrypted file's SHA-256
    # Reading public key to check signature with
    keyPair = RSA.importKey(open(sender_pubKey, "rb").read())
    data = s
    #print(s)
    hash = SHA256.new(data)
    if file=="":
        file=download+"email.txt"
    f=open(file.split('.')[0] + ".sig", "rb")
    signature=f.read()
    f.close()
    #os.remove(file.split('.')[0]+".sig")
    #print(signature)
    verifier = PKCS115_SigScheme(keyPair.publickey())
    os.remove(file.split('.')[0] + ".sig")
    try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
        return True
    except:
        print("Signature is invalid.")
        return False
    return False


########################################## Safe Zone ########







'''

download="C:/Users/AshishPC/Desktop/WattsApp/download"+"/"
upload="C:/Users/AshishPC/Desktop/WattsApp/upload"+"/"
private_folder="C:/Users/AshishPC/Desktop/WattsApp/private/receiver"+"/" #welll

senderPublicKey="sender_pubKey.pem"
senderPrivateKey="C:/Users/AshishPC/Desktop/WattsApp/private/sender"+"/"+"sender_keyPair.pem"


receiverPublicKey="receiver_pubKey.pem"
receiverPrivateKey="C:/Users/AshishPC/Desktop/WattsApp/private/receiver"+"/"+"receiver_keyPair.pem"




file=""#download+"sample.bin"
string=b'\x92\xb0\xee\xe4\x06\x953\x8c\x86;\x9du\x99T\xa6-\xcb\xd6\xd0\xa6d\x19A\xa6%Q\x8e'
state,msg=decipher(receiverPrivateKey,"12345",senderPublicKey,file,string)
print(msg)

#cleanUp(file + ".sig", file + ".key", file + ".bin")
'''
