import os
import demjson
from .assert_util import not_none as assert_not_none
from slogger import Logger
from .util import get_project_path, extract_project_path, get_config_path
from pathlib import Path
from fn import F
from .config import load_all_config

logger = Logger.getLogger(__name__)


def load(config_path):
    def convert(data):
        return {
            "name": "{}_{}".format(data["project_name"], data["role_name"]),
            "local": data["project_path"],
            "original_name": data["role_name"]
        }

    return [convert(data) for data in load_all_config(config_path)]

def build(roles, remote_host = None, remote_name = None):
    from jinja2 import Template
    def get_host(): return 'hosts: localhost' if remote_host == None else 'hosts: ' + remote_host
    def get_name(): return '''environment:
    PYTHONPATH: "/home/{remote_name}/.local/lib/python2.7/site-packages" '''.format(remote_name = remote_name) if remote_name else ""
    '''
build the roles into the entry yaml file
roles: a list for role. the sturcture of role can be reference in get_roles
'''
    return Template('''
---

- name: deploy
  {{ hosts }}
  become: true
  become_method: sudo
  {{ remote_name }}
  roles:
{% for role in objs %}    - {{role}}
{% endfor %}
...
  
''').render(objs = [role["name"] for role in roles], hosts = get_host(), remote_name = get_name())


def link(roles, path):
    '''
link the roles
'''
    def get_src(role):
        return os.path.join(role["local"], "deploy", "roles", role["original_name"])

    def create_folder(name, parent_path):
        def create(path):
            if os.path.exists(path):
                return path
            os.makedirs(path)
            return path
        return create(os.path.join(parent_path, name))
    
    def get_dest(role):
        return os.path.join(create_folder("roles", os.path.abspath(path)) , role["name"])
    
    def link_role(role):
        if not os.path.exists(get_dest(role)):
            os.symlink(os.path.abspath(get_src(role)), get_dest(role))
        
    [link_role(role) for role in roles]


def link_src_to_deploy(rolesdata):
    ''' link src folder to deploy/roles/main/files/src for deployment '''
    
    def link(project_folder, src_name, link_folder):
        def put(target_path):
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            return target_path
        
        def link_path(source_path, target_link_path):
            if os.path.exists(source_path) and not Path(target_link_path).is_symlink():
                os.symlink(source_path, target_link_path)

        link_path(os.path.abspath(os.path.join(project_folder, src_name)),  os.path.join(\
                                                                                         put(os.path.abspath(os.path.join(project_folder, link_folder))),\
                                                                                         src_name)\
        )
        
    [link(project_folder, "src", "deploy/roles/main/files") for project_folder in list(set([p["local"] for p in rolesdata]))]
        
