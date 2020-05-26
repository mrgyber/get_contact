import base64
import codecs
import hashlib
import hmac

from config import HMAC_KEY
from Crypto.Cipher import AES


class Cipher:
    def __init__(self, config):
        self.config = config

        self.update_config()
        self.BS = 16

        self.cipher_aes = None

    def update_config(self):
        self.cipher_aes = AES.new(codecs.decode(self.config.AES_KEY, 'hex'), AES.MODE_ECB)

    def create_signature(self, payload, timestamp):
        message = bytes(f"{timestamp}-{payload}", 'utf8')
        secret = bytes(HMAC_KEY, 'utf8')
        signature = base64.b64encode(hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest())
        return signature

    def encrypt_aes_b64(self, data):
        data = bytes(data + (self.BS - len(data) % self.BS) * chr(self.BS - len(data) % self.BS), 'utf8')
        return base64.b64encode(self.cipher_aes.encrypt(data)).decode()

    def decrypt_aes_b64(self, data):
        data = self.cipher_aes.decrypt(base64.b64decode(data)).decode()
        return data[0:-ord(data[-1])]
