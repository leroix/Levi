from base64 import urlsafe_b64encode, urlsafe_b64decode

from keyczar.keys import AesKey

import config

k = AesKey.Read(config.CRYPTO_KEY)

def encrypt(message):
    return urlsafe_b64encode(k.Encrypt(message))

def decrypt(cipher):
    return k.Decrypt(urlsafe_b64decode(cipher))

