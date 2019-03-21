import logging

'''
Customizer transformer
'''
def transform_before_parse(message):
    logging.info(" [custom transformer] ===> %s", message)
    #return message.replace('a', 'XX')
    return message

def transform_after_parse(data):
    logging.info(" [custom transformer] ===> %s", str(data))
    #if type(data) is dict:
    #    for k in data:
    #        data[k] = 'xxxxxxxxxxxxxxxxx_'
    return data
