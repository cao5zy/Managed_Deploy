import os
from codegenhelper import debug
import subprocess
import re

def get_project_name_from_url(giturl):
    def parseName(basename):
        return basename.split(".")[0] if len(basename.split(".")) == 2 and basename.split(".")[1] == "git" else basename
    return parseName(os.path.basename(giturl))

def get_tag(giturl, tag, location = os.getcwd(), ssh_key = None):
    def tag_cmd():
        return '-b "%s"' % tag

    def key_cmd():
        return "" if ssh_key == None else \
            'GIT_SSH_COMMAND="ssh -i %s"'%os.path.abspath(ssh_key)

    def git_cmd():
        return "git clone --single-branch --depth 1 %s" % giturl

    subprocess.call(debug(" ".join([key_cmd(), git_cmd(), tag_cmd()]), "git cmd"), shell=True, cwd=debug(location, "exe path"))
    
def get_code(giturl, ssh_key = None, location = os.getcwd()):
    debug("start to clone code of %s" % giturl)

    def is_ssh():
        return giturl.startswith('git')
    
    subprocess.call(debug('ssh -i {key_file} git clone {giturl}'.format(key_file=ssh_key, giturl=giturl),'command'), \
                    shell=True, \
                    cwd=location) if is_ssh() else \
                    subprocess.call(debug('git clone {giturl}'.format(giturl=giturl), 'command'), \
                                    shell=True, \
                                    cwd=location)
    
    
