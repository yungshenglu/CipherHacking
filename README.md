# Hacking the Cipher

This repository is the assignment in NCTU course "Network Security".

---
## Abstarct

Chosen cipher attack is an attack model that If an attacker can gather information by obtaining the decryption of cipertexts, attacker can then retrieve the plaintext without having the key. This repository is going to hack the cipher by RSA.

---
## Description

RSA is an important encryption technique first publicly invented by Ron Rivest, Adi Shamir, and Leonard Adleman in 1978. RSA security is based on the factoring problem -- the problem of factoring a large integer number into two prime numbers. In this project, each student is given a public key, an encrypted flag and a source code of the decrypter running on the server. Your goal is to use chosen ciphertext attack to retrieve the flag. The decrypt server is at `140.113.194.66`, port `8888`.

---
## Solutions

Use the concept of "chosen cyphertext attack" to hack the cipher. Because the public is know, so we can think that if we add some chosen text add the end of the ciphertext then after decryption we can get the original plaintext with adding chosen text.
1. Get the variable n and e from the public key
    * Use the function `getpubkey()` to get variables `n` and `e`
2. Read the ciphertext from `flag.enc`
    * Decode the ciphertext into `base64` binary string `C_binString`
    * Hexlify the binary string `C_binString` and transform into integer number `C`
3. Use RSA algorithm to calculate
    * Choose a number which is relatively prime with the `C`
    * Calculate the fake ciphertext `Y` by RSA algorithm
4. Connection to the server `140.113.194.66:8888` and receive the new ciphertext
    * Use the Python module [**pwn**](https://docs.pwntools.com/en/stable/about.html) to connect with server in function `connection(text)`
        ```bash
        # Installation
        $ apt-get update
        $ apt-get install python2.7 python-pip python-dev git libssl-dev libffi-dev build-essential
        $ pip install --upgrade pip
        $ pip install --upgrade pwntools
        ```
    * Receive the new cipher text
5. Transform the new ciphertext into plaintext
    * Decode the new ciphertext into binary string `C_binString`
    * Unhexlify the binary string `C_binString` and transform into integer number `C`
6. Use RSA algorithm to calculate the true plaintext
    * Use the function in Python module [**gmpy**](https://pypi.python.org/pypi/gmpy/1.15) to invert the chosen number before
    ```bash
    # Installation for Debian, Ubuntu
    $ sudo apt-get install libgmp-dev
    
    # Installation for Fedora, RedHat and CentOS
    $ yum install gmp-devel
    
    # Install gmpy
    $ pip install --upgrade pip
    $ pip install --upgrade gmpy
    ```
    * Calculate the true plaintext `Y` by RSA algorithm
    * Write the true plaintext into file `flag`
    ```bash
    # Flag
    FLAG{S0_y0u_d0_know_th3_cho5en_c1ph3r_4ttack!}
    ```

---
## File Description

* `src/decrypt.py` - The part of decryption on the server 140.113.194.66:8888
* `src/main.py` - Solution to hack the cipher
* `files/pub.pem` - The public key for RSA encryption
* `files/flag.enc` - The encryption of flag
* `out/flag` - The true plaintext

---
## Execution

```bash
# Execute the main.py for hacking the cipher
$ python main.py
[+] Opening connection to 140.113.194.66 on port 8888: Done
[*] Closed connection to 140.113.194.66 port 8888

# Show the true plaintext
$ cat flag
FLAG{S0_y0u_d0_know_th3_cho5en_c1ph3r_4ttack!}
```

---
## Author

* [David Lu](https://github.com/yungshenglu)

---
## License

[GNU GENERAL PUBLIC LICENSE Version 3](LICENSE)

> This repository is the assignment in NCTU course "Network Security". If you are taking this course, please do not duplicate from this repository. All rights reserved.