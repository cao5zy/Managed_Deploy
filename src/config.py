import os
import re
from fn import F
import demjson
from assertpy import assert_that
from slogger import Logger
from .util import get_project_path, extract_project_path, get_config_path

__logger__ = Logger.getLogger(__name__)

def load_all_config(config_path):
    '''
config_path: the path of the banyan configuration file
'''
    def get_cfg(dep_json):
        def load_cfg(cfg_path):
            return demjson.decode_file(cfg_path)

        return (F(get_config_path) >> F(load_cfg))(dep_json["project_name"], dep_json["config_name"] if "config_name" in dep_json else None)

    def get_roles(cfg_json, project_path):
        return [{"project_name": os.path.split(project_path)[1], \
                 "project_path": project_path,
                 "role_name": role_name} for role_name in cfg_json["roles_seq"]] if "roles_seq" in __logger__.title("get_roles cf_json").debug(cfg_json) else []
    
    def handle(cfg_json, depended_roles, project_path):
        try:
            return [y for x in [handle(get_cfg(dep), depended_roles, get_project_path(dep["project_name"])) for dep in cfg_json["dependencies"]] for y in x] \
                + get_roles(cfg_json, __logger__.title("get_roles_path_recursive").debug(project_path)) \
            if "dependencies" in cfg_json \
               else depended_roles + get_roles( \
                                                __logger__.title("no dep json").debug(cfg_json) \
                                                , __logger__.title("no dep path").debug(project_path) \
               )
        except Exception:
            __logger__.error("error happen in handle with project_path:%s\ncfg_json:%s" % (project_path, cfg_json))
            raise


    def put_all_db_first(roles):
        def get_db_roles():
            return list(filter(lambda n: is_db_role(n), roles))
        def get_non_db_roles():
            return list(filter(lambda n: not is_db_role(n), roles))

        return get_db_roles() + get_non_db_roles()
    
    return __logger__.title('load_all_config.result') \
                     .debug( \
                             (F(handle) \
                              >> F(put_all_db_first) \
                              )( \
                                 demjson.decode_file(config_path) \
                                 , [] \
                                 , extract_project_path(config_path) \
                                 ) \
                             )
               
def is_db_role(role, role_re=lambda n: re.match(r'.*db$', n)):
    assert_that(role).contains_key('role_name')

    return role_re(role['role_name']) is not None

    
def load_all_dependencies(config_path, handler):
    dependencies = lambda: "dependencies"
    
    def handle(dep_data):
        def handle_config(config_data):
            if dependencies() in config_data:
                [handle(dep) for dep in config_data[dependencies()]]
                
        handle_config(handler(dep_data))

    def handle_from_root(config_data):
        if dependencies() in config_data:
            [handle(dep) for dep in config_data["dependencies"]]

    handle_from_root(demjson.decode_file(config_path))
