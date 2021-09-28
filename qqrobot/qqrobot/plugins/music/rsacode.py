"""
姝よ剼鏈鍚戠綉鏄撲簯鎻愪氦鐨勮姹傜殑鍙傛暟杩涜鍔犲瘑
"""
import random
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

from nonebot.adapters.cqhttp.utils import escape

def aesEncrypt(text, secKey):

    blockSize = 16

    encryptor = AES.new(secKey.encode(), AES.MODE_CBC, b'0102030405060708')

    text = pad(text.encode(), blockSize)
    ciphertext = encryptor.encrypt(text)

    ciphertext = base64.b64encode(ciphertext)

    return str(ciphertext, encoding='utf-8')


def rsaEncrypt(text, pubKey, modulus):

    text = text[::-1]
    rs = int(binascii.b2a_hex(text.encode()), base=16) ** int(pubKey, base=16) % int(modulus, base=16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):

    str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    r = ''

    for i in range(1, size+1):
        r = r + str[random.randint(0, len(str) - 1)]
    return r

if __name__ == '__main__':
    print(escape("[CQ:image,file=plice1.jpg]",  escape_comma=True))