import os, base64

def env(name, default_value=None):
    return os.environ[name] if name in os.environ else default_value

def encode(data):
    return "%s" % base64.b64encode(str.encode(data)).decode("UTF-8")

def decode(data):
    return base64.b64decode(data).decode("UTF-8")

def is_not_none(value):
    return value is not None

def finditem(key, obj):
    #print('fi', key, '->', obj)
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = finditem(key, v)
            if item is not None:
                return item

def has_key(key, kv):
    v = kv
    for k in key.split('.'):
        v = finditem(k, v)
        if v is None:
            return False
    return True
