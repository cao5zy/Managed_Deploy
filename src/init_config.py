from .util import get_config_path, get_project_path
from fn import Stream
import os

def init_config(project_name, config_name):
    def get_role_names():
        return ",".join(['"' + dir + '"' for dir in os.listdir(os.path.join(get_project_path(project_name), "deploy", "roles"))])
    
    def gen_content():return '''{{
    "project_name": "{project_name}",
    "dependencies": [{{
        "project_name": "<project_name>",
        "git": "<git_url>",
        "config_name": "<configuration_name>"
    }}
    ],
    "roles_seq": [{roles_arr}],
    "predefined_variables": {{}}
}}
'''.format(project_name=project_name, roles_arr=get_role_names())

    open(get_config_path(project_name, config_name), 'w').write(gen_content())
