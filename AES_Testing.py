
# 모듈을 불러옵니다.
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# 암호화할 문자열을 일정 크기로 나누기 위해서, 모자란 경우 크기를 채워줍니다.
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[0:-s[-1]]

# AES 암호화를 담당할 클래스 입니다.
class AESCipher:

    # 클래스 초기화 - 전달 받은 키를 해시 값으로 변환해 키로 사용합니다.
    def __init__(self, key):
        self.key = key
        self.key = hashlib.sha256(key.encode()).digest()

    # 암호화 - 전달받은 평문을 패딩 후, AES 256 으로 암호화 합니다.
    def encrypt(self, raw):
        raw = raw.encode()
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    # # 복호화 - 전달 받은 값을 복호화 한후, 언패딩해 원문을 전달합니다.
    # def decrypt(self, enc):
    #     enc = base64.b64decode(enc)
    #     iv = enc[:16]
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return unpad(cipher.decrypt(enc[16:])).decode()