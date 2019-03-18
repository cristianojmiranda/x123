import os

def env(name, default_value=None):
    return os.environ[name] if name in os.environ else default_value
