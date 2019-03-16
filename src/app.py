from .banyan_opt import get_options
import sys
import os
from .deploy import build_deploy_script, run_deploy, deploy_config
import logging
logging.basicConfig(stream = sys.stdout, level = 'DEBUG')
from .util import init_root, get_deploy_path

init_root()

def run(options):
    def root_folder():
        return os.getcwd()
    
    def banyan_config_path():
        return os.path.join(root_folder(), options.projectname, "deploy", "dev.cfg" if options.cfg == None else options.cfg + ".cfg")

        
    def error_handler(msg):
        print(msg)

    def get_remote_dict():
        return {"key": options.key_file, "remote_user": options.user_name, "remote_addr": options.remote_addr} if \
            not (options.key_file == None or options.user_name == None or options.remote_addr == None) else None
        
    if options.command == "deploy":
        run_deploy(options.projectname, options.cfg, options.role_tags)
    elif options.command == "build":
        build_deploy_script(options.projectname, options.cfg, only_structure = options.only_structure, remote_dict = get_remote_dict(), gate = options.build_gate, proxy_mapping = options.proxy_mapping, noauth = options.noauth, authorization = options.authorization)
    elif options.command == "config":
        deploy_config(options.projectname, options.cfg)
    elif options.command == "get":
        from .get_code_with_tag import init_tag_for_project
        init_tag_for_project(options.giturl, options.tag, options.cfg, os.getcwd(), options.key_file)
    elif options.command == "init":
        from .init_config import init_config
        init_config(options.projectname, options.cfg)
    elif options.command == "clear":
        from .clear_deploy import clear_deploy
        clear_deploy(os.path.join(os.getcwd(), options.projectname), options.cfg)
    else:
        print('please set the valid command: deploy, init')
        
def main():
    run(get_options())
