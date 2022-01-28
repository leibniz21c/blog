#
#   Code from : https://github.com/ndo04343/crypto-post-module/blob/main/encoder.py
#   
###############################################################################
####### THIS SCRIPT WILL BE UESD AUTOMATICALLY, DO NOT MODIFY OR MOVE #########
###############################################################################

import sys
import base64

from urllib import parse
from Cryptodome import Random
from Cryptodome.Cipher import AES
from pkcs7 import PKCS7Encoder

def add_padding(byte_stream, total_size):
    if len(byte_stream) >= total_size: return byte_stream
    return byte_stream + b'\0'*(total_size - len(byte_stream))

def encrypt_data(data, key):
    # Add padding
    encryption_key = add_padding(str.encode(key), 16)
    
    # pad
    encoder = PKCS7Encoder()
    raw = encoder.encode(data) # Padding
    iv = Random.new().read(AES.block_size) #AES.block_size defaults to 16

    # no need to set segment_size=BLAH
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    encrypted_text = base64.b64encode(iv + cipher.encrypt(str.encode(raw))) 
    return encrypted_text

if __name__=="__main__":
    # arg check
    if len(sys.argv) != 4: 
        print("Usage: python3 {} [input_filename] [output_filename] [key]".format(sys.argv[0]))
        exit(0)
    
    # Input file
    with open(sys.argv[1], "r") as input_file:
        plain_text = input_file.read() # get plain text

        # Parse metadata
        meta_start = plain_text.find("---", 0)
        meta_end = plain_text.find("---", 1) + 4
        meta_data = plain_text[meta_start:meta_end]

        plain_text = parse.quote(plain_text[meta_end:]) # get plain text
        cipher_text = encrypt_data(plain_text, sys.argv[3]).decode('utf-8') # encrypt

        with open(sys.argv[2], "w") as output_file:
            output_file.write(meta_data + cipher_text)