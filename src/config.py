from fn import F
import os
import demjson
from .assert_util import not_none as assert_not_none
from slogger import Logger
from .util import get_project_path, extract_project_path, get_config_path
from pathlib import Path
from slogger import Logger

logger = Logger.getLogger(__name__)

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
                 "role_name": role_name} for role_name in cfg_json["roles_seq"]] if "roles_seq" in logger.title("get_roles cf_json").debug(cfg_json) else []
    
    def handle(cfg_json, depended_roles, project_path):
        try:
            return [y for x in [handle(get_cfg(dep), depended_roles, get_project_path(dep["project_name"])) for dep in cfg_json["dependencies"]] for y in x] + get_roles(cfg_json, logger.title("get_roles_path_recursive").debug(project_path)) \
            if "dependencies" in cfg_json \
               else depended_roles + get_roles(logger.title("no dep json").debug(cfg_json), logger.title("no dep path").debug(project_path))
        except Exception:
            logger.error("error happen in handle with project_path:%s\ncfg_json:%s" % (project_path, cfg_json))
            raise

    return handle(demjson.decode_file(config_path), [], extract_project_path(config_path))

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
