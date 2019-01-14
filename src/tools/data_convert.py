import os
import re

def encode_val(val):
    return val if type(val) is not str else '''"%s"''' % val
    
def dict2yml(dict_data):
    
    def gen_item(key, val):
        return "%s: %s" % (key, encode_val(val))
    
    return os.linesep.join([gen_item(key, val) for key, val in dict_data.items()]) if isinstance(dict_data, dict) else ""

def dict2assignments(dict_data):
    return ['''%s=%s''' % (key, val) \
                for key, val in dict_data.items()]
