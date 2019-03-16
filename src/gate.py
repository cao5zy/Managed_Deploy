from .config import load_all_config
from .util import get_project_path, extract_project_path, get_config_path
import os
import sys
from slogger import Logger
import demjson
from fn import F
import json
from functools import reduce
from assertpy import assert_that

logger = Logger.getLogger(__name__)

_auth_db_name = "auth_db"
_microservice_gate_name = "microservice_gate"

def build_gate(project_name, config_name, build_gate, proxy_mapping = None, noauth = None, authorization = None):
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
                
                
        return projects if len(projects) == 1 else [] if len(projects) == 0 else reduce(work, projects)
    

    def build_authorization(projects):
        '''
            authorization is one of the service
        '''
        def get_authorized_project():
            return list(filter(lambda n: n['project_name'] == authorization, projects))

        def get_proxy_mapping_projects():
            return list(filter(lambda n:n['has_customized_mapping'], projects))

        def get_no_auth_projects():
            return list(filter(lambda n:n['noauth'], projects))

        try:

            if authorization:
                return get_authorized_project() + \
                               get_proxy_mapping_projects() + \
                               get_no_auth_projects()
            else:
                return projects
        except Exception as ex:
            logger.title('build_authorization.error').error(ex)
            logger.title('build_authorization.error.data').error(projects)
            
            raise ex

    
    def data():
        def dumy(projects):
            assert_that(projects).is_not_empty()
            assert_that(projects[0]).contains_key('project_name', 'project_path', 'role_name')
            
            return {
                "project_name": "roles",
                "items": (F(remove_duplicate) >> \
                          F(proxy_mapping) >> \
                          F(root_path_at_last) >> \
                          F(no_auth) >> \
                          F(build_authorization) >> \
                          F(remove_duplicate) \
                )(projects)
            }
        return dumy(load_all_config(get_config_path(project_name, config_name)))

    def build_no_auth_list():
        return [] if noauth == None else \
            noauth if isinstance(noauth, list) else \
            [noauth]
    
    def no_auth(all_config, no_auth_list = build_no_auth_list()):
        def build(item):
            item['noauth'] = True if item['project_name'] in no_auth_list else False
            return item

        return list(map(lambda item: build(item), all_config))
    def build_mapping():
        '''convert the data
[a:b] to 
[[a,b]] '''
        return [] if proxy_mapping == None else \
            list(map(lambda item: [item.split(':')[0], item.split(':')[1]], proxy_mapping if isinstance(proxy_mapping, list) else [proxy_mapping]))
    
    def proxy_mapping(all_config, mapping = build_mapping()):
        def get_mapping(item):
            return list(filter(lambda obj: obj[0] == item['project_name'], mapping))
        
        def build(item):
            return {
                'project_name': item['project_name'],
                'project_path': item['project_path'],
                'role_name': item['role_name'],
                'proxy_mapping': '/_api/{}/'.format(item['project_name']) if len(get_mapping(item)) == 0 else get_mapping(item)[0][1],
                'has_customized_mapping': len(get_mapping(item)) > 0
            }

        return list(map(lambda item: build(item), all_config))

    def root_path_at_last(all_config):
        '''make sure the root path / is at the last'''
        sorted_list = sorted(all_config, key = lambda n:n['proxy_mapping'])
        sorted_list.reverse()
        return sorted_list
        
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
        try:
            with open(get_config_path(project_name, config_name), 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            logger.title('save_config.error').error(e)
            logger.title('save_config.data').error(config_data)
            
    def modify_config(remove):
        (F(open_config) >>\
            F(update_config, remove) >>\
            F(save_config)
         )()
    def gen_template():
        from md_codegen import run
        run(logger.title('gen_template.output_path').debug(output_path()), \
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

    try:
        
        if logger.title('build_gate').debug(build_gate) == True:
            remove_gate()
            gen_template()
        else:
            remove_gate()
    except Exception as e:
        import traceback
        logger.title('build_gate.error.trackback').error(''.join(traceback.format_tb(e.__traceback__)))
        logger.title('build_gate.error').error(e)

        

