#!/usr/bin/env python2

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
import sys, os, signal
import binascii

# Alarm function
def alarm(time):
    def handler(signum, frame):
        print 'Timeout. Bye~'
        exit()
    
    # Set the signal handler and alarm
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(time)
    
# Get public key
def getpubkey():
    with open('./pub.pem', 'rb') as f:
        pub = f.read()
        key = RSA.importKey(pub)
    return key

# Check if u send me the flag !
def check(cipher_text, pubkey):
    with open('./flag', 'r') as f:
        flag = f.read().strip()

        # Use binascii.hexlify to transfer byte string into integer then use RSA to encrypt it
        flag_enc = pubkey.encrypt(int(binascii.hexlify(flag), 16), '')[0]
        d = SHA256.new()
        dd = SHA256.new()

        # Use binascii.unhexlify to transfer integer into byte string
        d.update(binascii.unhexlify(hex(flag_enc)[2 : -1]))
        try :
            dd.update(base64.b64decode(cipher_text))
        except TypeError:
            print 'base64 decode error!'
            sys.exit()

        if d.hexdigest() == dd.hexdigest():
            return 0
        return 1

# decrypt the cipher_text you send
def decrypt(cipher_text):
    with open('./pub.pem', 'rb') as f:
        pub = f.read()
        key = RSA.importKey(pub)

        try :
            text = key.decrypt(base64.b64decode(cipher_text))
        except TypeError:
            print 'base64 decode error!'
            sys.exit()

        print 'Decrypted message in base64 encoding format: '
        print base64.b64encode(text)

if __name__ == '__main__' :
    # Set the signal handler and a 60-second alarm
    alarm(60)

    sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", 0)
    key = getpubkey()

    # Input hint
    cipher_text = raw_input('Give me your encrypted message in base64 encoding format : ').strip()

    if check(cipher_text, key) :
        decrypt(cipher_text)
    else :
        print 'You wish!'
