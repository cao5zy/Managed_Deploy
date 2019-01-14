import os

class DeployInfo:
    def __init__(self, deploy_folder_path):
        self.playbook_name = lambda: 'main.yml'
        self.host_file_name = lambda: 'main.host'

        self.playbook_path = lambda: os.path.join(deploy_folder_path, self.playbook_name())
        self.host_file_path = lambda: os.path.join(deploy_folder_path, self.host_file_name())

        self.deploy_folder_path = lambda: deploy_folder_path
