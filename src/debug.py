import os

debug_flag = "BANYAN_DEBUG"
def simple(obj, title = None):
    if os.environ.get(debug_flag):
        if title:
            print("%s:%s"%(title, obj))
        else:
            print(obj)
    return obj
    

def on():
    os.environ[debug_flag] = "debug"

def off():
    os.environ[debug_flag] = None
