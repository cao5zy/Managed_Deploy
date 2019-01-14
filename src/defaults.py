import os
import yaml
import functools
from .debug import simple
from jinja2 import Template
from fn import F

def all(parent_folder, role_names = []):
    def get_role_names(roles_path):
        def get_roles():
            return [y for x in [dirs for root, dirs, _ in os.walk(roles_path, followlinks = True) if root == roles_path] for y in x]

        return get_roles() if os.path.exists(roles_path) else []
    
    def get_defaults_by_name(rolename):
        def get_defaults(path):
            return yaml.load(open(path, 'r')) if os.path.exists(path) else {}

        return (F(lambda title, content: simple(content, title), "get_defaults_by_name_path") >> \
                F(get_defaults) >> \
                F(lambda title, content: simple(content, title), "get_defaults_by_name") >> \
                F(init_root, rolename) >> \
                F(lambda title, content: simple(content, title), "init_root") \
                )(os.path.join(parent_folder, "roles", rolename, "defaults", "main.yml")) \
                if len(role_names) == 0 or rolename in role_names else {}
                
    def combine(names):
        return functools.reduce(lambda a, b: {**a, **b}, names)
    return combine([get_defaults_by_name(rolename) for rolename in get_role_names(os.path.join(parent_folder, "roles"))])

def init_root(role_name, default_values):
    def get_project_name():
        return None if len(role_name.split('_')) < 2 else (lambda elements:"_".join(elements[0:len(elements)-1]))(role_name.split('_'))

    def init_root(key, value):
        return value if not key.endswith('_root') else os.path.join(os.getcwd(), get_project_name())
    
    assert get_project_name() != None, "role_name:%s is not in format like <project_name>_<role_name>" % role_name

    def write_root(new_values):
        for key in default_values:
            new_values[key] = init_root(key, default_values[key])

        return new_values
    
    return write_root({})

def write(file_path, keyvals, remote_addr = None):
    from .tools.data_convert import dict2assignments

    def get_remote_addr(): return '' if remote_addr == None else '[remote]' + os.linesep + remote_addr
    
    file = open(file_path, 'w')
    try:
        file.write(Template('''[all:vars]
{% for assignment in assignments %}{{assignment}}
{% endfor %}

{{remote_addr}}
''').render(assignments = dict2assignments(keyvals), remote_addr = get_remote_addr()))
        
    finally:
        file.close()

def override_values(cfg_json, host_values):
    def override(new_values):
        simple(host_values, "override_values_host_values").update(new_values)
        return host_values

    return override(cfg_json["predefined_variables"]) \
        if "predefined_variables" in cfg_json \
           else simple(host_values, "override_values_host_values")
        

