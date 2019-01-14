from .config import load_all_config
from .util import get_project_path, extract_project_path, get_config_path
import os
import sys
from slogger import Logger
import demjson
from fn import F
import json
from functools import reduce

logger = Logger.getLogger(__name__)

_auth_db_name = "auth_db"
_microservice_gate_name = "microservice_gate"

def build_gate(project_name, config_name, build_gate):
    def remove_duplicate(projects):
        def work(result, item):
            if isinstance(result, list):
                if len(list(filter(lambda obj:obj['project_name'] == item['project_name'], result))) != 0:
                    return result
                else:
                    return result + [item]
            else:
                if result['project_name'] == item['project_name']:
                    return [result]
                else:
                    return [result, item]
                
                
        return reduce(work, projects)
    
    def data():
        return {
            "project_name": "roles",
            "items": remove_duplicate(load_all_config(get_config_path(project_name, config_name)))
        }
    
    def output_path():
        return os.path.join(get_project_path(project_name), "deploy")

    def template_path():
        return os.path.join(os.path.split(os.path.realpath(__file__))[0], "./auth_template")


    def open_config():
        return demjson.decode_file(get_config_path(project_name, config_name))

    def update_config(remove, config_data):
        roles_seq = [item for item in logger.title("origin_roles_seq").debug(config_data["roles_seq"]) if item not in [_auth_db_name, _microservice_gate_name]]
        
        config_data["roles_seq"] = logger.title("pure_roles_seq").debug(roles_seq) + ([] if remove else [_auth_db_name, _microservice_gate_name])
        
        return config_data

    def save_config(config_data):
        with open(get_config_path(project_name, config_name), 'w') as f:
            json.dump(config_data, f, indent=4)

            
    def modify_config(remove):
        (F(open_config) >>\
            F(update_config, remove) >>\
            F(save_config)
         )()
    def gen_template():
        from md_codegen import run
        run(output_path(), \
            "",\
            None,\
            None,\
            None, \
            None,\
            None,\
            demjson.encode(data()),\
            None,\
            template_path(),\
            check_repo = False)

        modify_config(False)
        
    def remove_gate():
        import shutil

        def remove_folder(roles_folder):
            [lambda path: shutil.rmtree(os.path.join(roles_folder, path)) for path in [_auth_db_name, _microservice_gate_name] \
             if os.path.exists(os.path.join(roles_folder, path))]
            
        remove_folder(os.path.join(get_project_path(project_name), "deploy", "roles"))
        
        modify_config(True)

    if logger.title('build_gate').debug(build_gate) == True:
        remove_gate()
        gen_template()
    else:
        remove_gate()

        

