from codegenhelper import remove
import os

def clear_deploy(projectpath, config_name):
    def clear(path):
        if os.path.exists(path):
            remove(path)
    clear(os.path.join(projectpath, "deploy", "." + config_name))
