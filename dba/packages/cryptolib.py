from Crypto.PublicKey import RSA

def GenerateKeys(password,path,file_name):
    keyPair = RSA.generate(1024)

    f = open(path+file_name+"_keyPair.pem", "wb")
    f.write(keyPair.exportKey(passphrase=password))
    f.close()

    s=keyPair.publickey().exportKey()
    return s #returning public key as binary string
