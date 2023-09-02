from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


# 生成随机的AES密钥
def generate_key():
    return get_random_bytes(16)


# PKCS7填充
def pad(data):
    length = AES.block_size - (len(data) % AES.block_size)
    return data + chr(length) * length


# PKCS7去填充
def unpad(padded_data):
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]


def encrypt_ecb(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data


def decrypt_ecb(key, encrypted_data):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data)


# 加密数据
def encrypt_ecb_b64(key, data):
    data = encrypt_ecb(key, data)
    b64_data = base64.b64encode(data)
    return b64_data


# 解密数据
def decrypt_ecb_b64(key, data):
    data = decrypt_ecb(key, data)
    b64_data = base64.b64decode(data)
    return b64_data


def encrypt_cbc(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data


def decrypt_cbc(key, iv, encrypted_data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return unpad(decrypted_data)


# 加密数据
def encrypt_cbc_b64(key, iv, data):
    datas = decrypt_cbc(key, iv, data)
    b64_data = base64.b64encode(datas)
    return b64_data


# 解密数据
def decrypt_cbc_b64(key, iv, encrypted_data):
    datas = decrypt_cbc(key, iv, encrypted_data)
    b64_data = base64.b64decode(datas)
    return b64_data
