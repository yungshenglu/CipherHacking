#!/usr/bin/env python2

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from pwn import *
import base64
import sys, os, signal
import binascii
import gmpy

# Get public key
def getpubkey():
    with open('./pub.pem', 'rb') as f:
        pub = f.read()
        key = RSA.importKey(pub)
    return key

# Connect to remote server 140.113.194.66:8888
def connection(text):
    conn = remote('140.113.194.66', 8888)
    conn.sendline(text)
    conn.recvline()

    # Return new flag
    return conn.recvline()


# Main function
if __name__ == '__main__':
    sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", 0)
    key = getpubkey()

    # Get the variable n and e from pub.pem
    n = key.n
    e = key.e

    with open('./flag.enc', 'rb') as f:
        flag = f.read().strip()

        # Get the binary string from flag.enc
        C_binString = base64.b64decode(flag)
        C = int(binascii.hexlify(C_binString), 16)

        # RSA algorithm
        X = 100
        Y = binascii.unhexlify(hex(C * (X ** e) % n)[2 :])

        # Connect to remote server and send the Y
        flag = connection(base64.b64encode(Y))

        # Transform the new ciphertext into plaintext
        C_binString = base64.b64decode(flag[: -1])
        C = int(binascii.hexlify(C_binString), 16)

        # Calculate the RSA
        X = gmpy.invert(X, n)
        Y = binascii.unhexlify(hex(C * X % n)[2 :])

        # Write into file - flag
        file = open("flag", "a")
        file.write(Y)
        file.close()