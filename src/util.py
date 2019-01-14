import os
import shutil
from .assert_util import not_none as assert_not_none

env_dict = {}

def init_root(path = None):
    env_dict["root_path"] = os.getcwd() if path == None else os.path.abspath(path)
    
def get_root():
    return env_dict["root_path"]

def extract_project_path(config_path):
    import re
    def match(pattern):
        return re.match(pattern, config_path)[0] if re.match(pattern, config_path) else None
    return os.path.abspath(assert_not_none(match('''.*(?=/deploy/\w+\.cfg)'''), "cfg path is invalid. Please make sure the it is under project folder"))

def get_project_path(project_name):
    return os.path.abspath(os.path.join(get_root(), project_name))

def get_config_path(project_name, config_name = None):
    return os.path.abspath(os.path.join(get_root(), project_name, "deploy", "dev.cfg" if config_name == None else config_name + ".cfg"))

def get_deploy_path(project_name, config_name = None):
    return os.path.abspath(os.path.join(get_root(), project_name, "deploy", ".dev" if config_name == None else "." + config_name))

def get_deploy_host(project_name, config_name = None):
    return os.path.join(get_deploy_path(project_name, config_name), "main.host")

def get_deploy_yml(project_name, config_name = None):
    return os.path.join(get_deploy_path(project_name, config_name), "main.yml")

def get_deploy_ansible_cfg_path(project_name, config_name = None):
    return os.path.join(get_deploy_path(project_name, config_name), "ansible.cfg")
