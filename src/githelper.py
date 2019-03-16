import os
from slogger import Logger
import subprocess
import re
from assertpy import assert_that

logger = Logger.getLogger(__name__)

def get_project_name_from_url(giturl):
    def parseName(basename):
        return basename.split(".")[0] if len(basename.split(".")) == 2 and basename.split(".")[1] == "git" else basename
    return parseName(os.path.basename(giturl))

def get_tag(giturl, tag, location = os.getcwd(), ssh_key = None):
    assert_that(location).exists()
    assert_that(tag).is_not_empty()
    assert_that(giturl).is_not_empty()
    
    def tag_cmd():
        return '-b "%s"' % tag

    def key_cmd():
        return "" if ssh_key == None else \
            'GIT_SSH_COMMAND="ssh -i %s"'%os.path.abspath(ssh_key)

    def git_cmd():
        return "git clone --single-branch --depth 1 %s" % giturl

    subprocess.call(logger.title('get_tag cmd').debug(" ".join([key_cmd(), git_cmd(), tag_cmd()])), shell=True, cwd=logger.title('current path').debug(location))
    
def get_code(giturl, ssh_key = None, location = os.getcwd()):
    assert_that(giturl).is_not_empty()
    assert_that(location).exists()
    def is_ssh():
        return giturl.startswith('git')
    
    subprocess.call(logger.title('get_code ssh cmd').debug('ssh -i {key_file} git clone {giturl}'.format(key_file=ssh_key, giturl=giturl)), \
                    shell=True, \
                    cwd=location) if is_ssh() else \
                    subprocess.call(logger.title('get_code cmd').debug('git clone {giturl}'.format(giturl=giturl)), \
                                    shell=True, \
                                    cwd=location)
    
    
