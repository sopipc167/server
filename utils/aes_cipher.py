import base64
import hashlib

from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

import configparser

config = configparser.ConfigParser()
config.read_file(open('config/config.ini'))
SECRET_KEY = config['database']['encryption_key']

class AESCipher:
    def __init__(self):
        self.BS = 16
        self.key = hashlib.sha256(SECRET_KEY.encode('utf-8')).digest()
        self.iv = Random.new().read(AES.block_size)

    def encrypt(self, raw):
        raw = pad(raw.encode('utf-8'), AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))
        
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(cipher.decrypt(enc), AES.block_size)

    def encrypt_str(self, raw):
        if raw is None or raw == '':
            return None
        return self.encrypt(raw).decode('utf-8')

    def decrypt_str(self, enc):
        if enc is None or enc == '':
            return None
        if type(enc) == str:
            enc = str.encode(enc)
        return self.decrypt(enc).decode('utf-8')
