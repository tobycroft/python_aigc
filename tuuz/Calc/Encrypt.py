import base64
import hashlib
import hmac


def md5(string):
    return hashlib.md5(string.encode()).hexdigest()


def md5_up(string):
    return md5(string).upper()


def sha1(string):
    return hashlib.sha1(string.encode()).hexdigest()


def sha256(string):
    return hashlib.sha256(string.encode()).hexdigest()


def sha512(string):
    return hashlib.sha512(string.encode()).hexdigest()


def hmac_sha256(message, secret):
    key = bytes(secret, 'utf-8')
    message = bytes(message, 'utf-8')
    h = hmac.new(key, message, hashlib.sha256)
    return base64.b64encode(h.digest()).decode()
