import os

def put_folder(path):
    '''
if the path of the folder doesn't exist, it will create the folder.
the function will return the path
'''
    if not os.path.exists(path):
        os.makedirs(path)
    return path
