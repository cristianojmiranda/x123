import logging, os, base64

def env(name, default_value=None, parser=str):
    _val = os.environ[name] if name in os.environ else default_value
    logging.info("ENV %s => %s" % (name, str(_val)))
    return parser(_val)
