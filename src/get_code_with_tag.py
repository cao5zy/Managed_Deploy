import os
from .githelper import get_tag, get_project_name_from_url
from .config import load_all_dependencies
import demjson

def init_tag_for_project(giturl, tag, config_name, location=os.getcwd(), key_file_path = None):
    get_tag(giturl, tag, location, key_file_path)

    def load_tag(dep_config):
        get_tag(dep_config["giturl"], dep_config["tag"], location, key_file_path)
        
        return demjson.decode_file(os.path.join(location, get_project_name_from_url(dep_config["giturl"]), "deploy", dep_config["config_name"] + ".cfg"))
    
    load_all_dependencies(os.path.join(location, get_project_name_from_url(giturl), "deploy", config_name + ".cfg"), load_tag)
