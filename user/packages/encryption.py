import os
import sys
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Random import random
from Crypto.Signature import PKCS1_v1_5

def file_read(file):
    f = open(file, "r")
    content = f.read()
    f.close()
    return content

def inp(password,file_name):
    keyPair = RSA.generate(1024)

    f = open(file_name+"_keyPair.pem", "wb")
    f.write(keyPair.exportKey(passphrase=password))
    f.close()

    f = open(file_name+"_pubKey.pem", "wb")
    s=keyPair.publickey().exportKey()
    #print(s)
    f.write(s)
    f.close()

def sigGenerator(sender_keyPair, file, sender_passphrase):
    # Opening and reading file to encrypt
    buffer = file_read(file)
    # Creating hash of the file. Using SHA-256 (SHA-512 rose problems)
    h = SHA256.new(buffer.encode())
    # Reading private key to sign file with
    keyPair = RSA.importKey(open(sender_keyPair, "rb").read(),passphrase=sender_passphrase)
    #key = RSA.importKey(open("public.pem", "rb"))
    keySigner = PKCS1_v1_5.new(keyPair)
    print ( h.hexdigest())
    print ( h.hexdigest())
    # Saving signature to *.sig file
    sign=str(keySigner.sign(h))
    #print(sign)
    f = open(file.split('.')[0] + ".sig", "w")
    f.write(sign)
    f.close()

def keyGenerator(reveiver_pubKey, file, iv):
    # Generating 1024 random bits, and creating SHA-256 (for 32 bits compatibility with AES) to be used as session key
    h = SHA256.new(str(random.getrandbits(1024)).encode())
    # Reading public key to encrypt AES key with
    #recipient_key = RSA.import_key(open("receiver.pem").read())
    '''pudbkey= RSA.importKey(open(reveiver_pubKey))
    pubkey=key.exportKey()
    return pubkey'''

    #secret_code = "123"
    encoded_key = open(reveiver_pubKey, "rb").read()
    pubkey = RSA.import_key(encoded_key)
    keyCipher = PKCS1_OAEP.new(pubkey)
    # Saving encrypted key to *.key file
    f = open(file.split('.')[0] + ".key", "wb")
    f.write(iv + keyCipher.encrypt(h.digest()))
    f.close()
    # Returning generated key to encrypt file with
    return h.digest()


def encipher(sender_keyPair,reveiver_pubKey, file, sender_passphrase):
    # Opening file to encrypt in binary reading mode
    f = open(file, "rb")
    buffer = f.read()
    f.close()
    # Generating file's signature (and saving it)
    sigGenerator(sender_keyPair, file, sender_passphrase)
    # Generating initializing vector for AES Encryption
    iv = Random.new().read(AES.block_size)
    # Generating symmetric key for use (and saving it)
    k=keyGenerator(reveiver_pubKey, file, iv)
    #k = k.encode()
    # Encrypting and saving result to *.bin file. Using CFB mode
    keyCipher = AES.new(k, AES.MODE_CFB, iv=iv)
    cipherText=keyCipher.encrypt(buffer)
    f = open(file.split('.')[0] + ".bin", "wb")
    f.write(cipherText)
    f.close()


#inp("123","sender")
#inp("12345","receiver")
#encipher("sender_keyPair.pem","receiver_pubKey.pem","abc.txt", "123")
