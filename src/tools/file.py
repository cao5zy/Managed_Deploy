import os
from .folder import put_folder

def get_file_name(path):
    return os.path.split(path)[1]

def get_file_only_name(path):
    return get_file_name(path).split('.')[0]

def put_file(path):
    '''
make sure the folder of the file exists
'''
    return os.path.join(put_folder(os.path.dirname(path)), \
                        get_file_name(path) \
                        )

        
        
