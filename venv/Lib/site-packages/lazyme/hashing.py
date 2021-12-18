
import hashlib

def md5(s, digest='int'):
    """From https://stackoverflow.com/a/13213664/610569"""
    if digest == 'int':
        return int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16)
    elif digest == 'binary':
        return bin(int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16))[2:]
    else:
        return hashlib.md5(s.encode('utf-8')).hexdigest()
