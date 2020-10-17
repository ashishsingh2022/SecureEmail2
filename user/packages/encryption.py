import os
import sys
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Signature import PKCS1_v1_5

def file_read(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    return content


def sigGenerator(sender_keyPair, sender_passphrase,file="",string=""):
    # Opening and reading file to encrypt
    buffer = string
    #print("String before hash ")
    #print(buffer.encode())
    # Creating hash of the file. Using SHA-256 (SHA-512 rose problems)
    h = SHA256.new(buffer.encode())
    # Reading private key to sign file with
    f=open(sender_keyPair, "rb")
    keyPair = RSA.importKey(f.read(),passphrase=sender_passphrase)
    f.close()
    #key = RSA.importKey(open("public.pem", "rb"))
    keySigner = PKCS115_SigScheme(keyPair)
    #print ( h.hexdigest())
    # Saving signature to *.sig file
    sign=keySigner.sign(h)
    #print(sign)
    if file=="":
        file=upload+"email.txt"
    else:
        file=upload+file
    #print(sign)
    f = open(file.split('.')[0] + ".sig", "wb")
    f.write(sign)
    f.close()

def keyGenerator(reveiver_pubKey, file, iv):
    # Generating 1024 random bits, and creating SHA-256 (for 32 bits compatibility with AES) to be used as session key
    h = SHA256.new(str(random.getrandbits(1024)).encode())
    if file=="":
        file=upload+"email.txt"
    else:
        file=upload+file
    # Reading public key to encrypt AES key with
    #recipient_key = RSA.import_key(open("receiver.pem").read())
    '''pudbkey= RSA.importKey(open(reveiver_pubKey))
    pubkey=key.exportKey()
    return pubkey'''


    encoded_key = reveiver_pubKey
    pubkey = RSA.import_key(encoded_key)
    keyCipher = PKCS1_OAEP.new(pubkey)
    # Saving encrypted key to *.key file
    f = open(file.split('.')[0] + ".key", "wb")
    f.write(iv + keyCipher.encrypt(h.digest()))
    f.close()
    # Returning generated key to encrypt file with
    return h.digest()


def encipher(sender_keyPair,reveiver_pubKey,sender_passphrase,file_name="",string=""):
    # Opening file to encrypt in binary reading mode
    file=file_name
    buffer=string
    if file_name!="":
        f = open(upload+file, "r")
        buffer = f.read()
        f.close()
    # Generating file's signature (and saving it)
    sigGenerator(sender_keyPair,sender_passphrase,file,buffer)
    # Generating initializing vector for AES Encryption
    iv = Random.new().read(AES.block_size)
    # Generating symmetric key for use (and saving it)
    k=keyGenerator(reveiver_pubKey, file, iv)
    #k = k.encode()
    # Encrypting and saving result to *.bin file. Using CFB mode
    keyCipher = AES.new(k, AES.MODE_CFB, iv=iv)
    cipherText=keyCipher.encrypt(buffer.encode())
    if file=="":
        file=upload+"email.txt"
    else:
        file=upload+file
        f = open(file.split('.')[0] + ".bin", "wb")
        f.write(cipherText)
        f.close()
        os.remove(file)
    return cipherText



upload="temp/"
private_folder="private/"






#file=""
#string="Apple is my favourite fruit"
#s=encipher(senderPrivateKey,receiverPublicKey,"123",file, string)
#print(s)
