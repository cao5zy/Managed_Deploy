import os
from .defaults import write as write_defaults, override_values, all as all_defaults
from .roles import build as roles_build, link as roles_link, load as roles_load, link_src_to_deploy
import yaml
from .tools.file import get_file_name, get_file_only_name, put_file
from .tools.folder import put_folder
import demjson
from fn import _, F, iters
from .tools.dicthelper import update_dict
from .util import get_config_path, get_deploy_path, get_deploy_host, get_deploy_ansible_cfg_path
from .tools.data_convert import dict2assignments
import json
from slogger import Logger
from .deploy_info import DeployInfo

logger = Logger.getLogger(__name__)

def run_deploy(project_name, config_name, tags = None):
    '''configuration_path: it is the folder path which contains the main.sh to launch the deploy script'''
    import subprocess

    def run(deployInfo):
        def build_base_command():
            return "sudo ansible-playbook ./{yml_file} -i ./{host_file}".format(yml_file = deployInfo.playbook_name(), host_file = deployInfo.host_file_name())

        def build_tag(base_command):
            return base_command if tags == None or len(tags) == 0 else \
                '{base_command} --tags "{tags}"'.format(base_command = base_command, tags = ",".join(tags))
        
        p = subprocess.Popen((F(build_base_command) >> F(build_tag))(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = deployInfo.deploy_folder_path())

        while p.poll() is None:
            line = p.stdout.readline()
            if line:
                print(line.strip())

    run(DeployInfo(get_deploy_path(project_name, config_name)))

def build_deploy_script(project_name, config_name, only_structure=False, remote_dict = None, gate = False):
    from .gate import build_gate
    
    build_gate(project_name, config_name, gate)
    build_deploy_script_internal(project_name, config_name, only_structure, remote_dict)
    
def build_deploy_script_internal(project_name, config_name, only_structure=False, remote_dict = None):
    deploy_path = lambda:get_deploy_path(project_name, config_name)
    deployInfo = DeployInfo(deploy_path())
    
    def yml_file_folder(): return put_folder(os.path.abspath(deploy_path()))
    def bash_file(): return os.path.join(yml_file_folder(), get_file_only_name(deployInfo.playbook_path()) + ".sh")
    def get_roles_data():return roles_load(logger.title("config_path").debug(get_config_path(project_name, config_name)))
    def write_playbook(content): open(put_file(deployInfo.playbook_path()), 'w').write(content)

    # write data to file
    write_playbook(roles_build(get_roles_data(), remote_host = None if remote_dict == None else 'remote', remote_name = remote_dict["remote_user"] if remote_dict else None))
    # build link for role folders

    roles_link(get_roles_data(), \
               logger.title("link_root").debug(yml_file_folder()) \
    )

    # link src folder to deploy/roles/main/files/src for deployment
    link_src_to_deploy(get_roles_data())

    def default_vals(): return all_defaults(yml_file_folder(), [role["name"] for role in get_roles_data()])

    # build inventory files on roles
    write_defaults(deployInfo.host_file_path(), default_vals(), remote_addr = None if remote_dict == None else remote_dict["remote_addr"])

    # write the defaults to cfg file
    (F(lambda config_path: demjson.decode_file(config_path)) >> \
        F(lambda new_vals, old_json: update_dict(old_json, new_vals), {} if only_structure else {"predefined_variables": default_vals()}) >> \
        F(lambda json_data: json.dumps(json_data, indent=4, ensure_ascii=False)) >> \
        F(lambda content: open(get_config_path(project_name, config_name), 'w').write(content)))(get_config_path(project_name, config_name))


    def build_ansible_cfg():
        if remote_dict == None:
            return

        open(get_deploy_ansible_cfg_path(project_name, config_name), 'w').write('''[defaults]
remote_user={remote_user}
private_key_file={key_file}
host_key_checking=False
'''.format(remote_user=remote_dict["remote_user"], key_file=remote_dict["key"]))
        
    build_ansible_cfg()


def deploy_config(project_name, config_name):
    import configparser
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(get_deploy_host(project_name, config_name))
    
    def get_banyan_config():
        return demjson.decode_file(get_config_path(project_name, config_name))
    def get_predefined_variables(banyan_config):
        return banyan_config["predefined_variables"] if "predefined_variables" in banyan_config else {}

    def set_config(updatedDict):
        config["all:vars"] = updatedDict
        return config
    
    def save_items_to_host(cfg):
        cfg.write(open(get_deploy_host(project_name, config_name), 'w'))

    (F(get_banyan_config) >> \
        F(get_predefined_variables) >> \
        F(update_dict, dict(config["all:vars"])) >> \
        F(set_config) >> \
        F(save_items_to_host))()

    


