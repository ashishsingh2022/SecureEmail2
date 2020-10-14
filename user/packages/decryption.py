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
    keyPair = RSA.importKey(open(receiver_keyPair, "r").read(), passphrase=receiver_passphrase)
    keyDecipher = PKCS1_OAEP.new(keyPair)
    # Reading iv and symmetric key used during encryption
    f = open(file.split('.')[0] + ".key", "rb")
    iv = f.read(16)
    k = keyDecipher.decrypt(f.read())
    return k, iv

def decipher(receiver_keyPair, file, receiver_passphrase):
    # Getting symmetric key used and iv value generated at encryption process
    k, iv = keyReader(receiver_keyPair, file, receiver_passphrase)
    # Deciphering the initial information and saving it to file with no extension
    keyDecipher = AES.new(k, AES.MODE_CFB, iv)
    bin = open(file + ".bin", "rb").read()
    f = open(file.split('.')[0]+"_decrypted.txt", "wb")
    f.write(keyDecipher.decrypt(bin))
    f.close()

def sigVerification(sender_pubKey, file):
    # Generating decrypted file's SHA-256
    h = SHA256.new()
    h.update(open(file, "r").read().encode())
    # Reading public key to check signature with
    keyPair = RSA.importKey(open(sender_pubKey, "rb").read())
    data = open(file, "r").read().encode()
    hash = SHA256.new(data)
    verifier = PKCS115_SigScheme(keyPair.publickey())
    try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
        return True
    except:
        print("Signature is invalid.")
        return False
    return False

def cleanUp(sig, key, bin):
    # Removing all of the files created, except for the final deciphered file
    os.remove(sig)
    os.remove(key)
    os.remove(bin)

########################################## Safe Zone ########

file="abc"
decipher("receiver_keyPair.pem", file,"12345")
#cleanUp(file + ".sig", file + ".key", file + ".bin")
