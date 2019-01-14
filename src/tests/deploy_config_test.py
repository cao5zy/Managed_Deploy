from nose import with_setup
from codegenhelper import init_test_folder, remove_test_folder, test_root, debug, put_folder, put_file
from fn import F, _
import os
from assertpy import assert_that, contents_of
from ..deploy import build_deploy_script, deploy_config
import demjson
from ..util import init_root

init_root(test_root())
def setup_deploy():
    init_test_folder()
    project_folder = F(put_folder, "project1") >> F(put_folder, "deploy")
    put_file("main.host", \
             (project_folder >> F(put_folder, ".dev"))(test_root()),\
             '''[all:vars]
name1=a b
name2=b
name3=c

[remote]
1.1.1.1
 ''')
    put_file("dev.cfg", \
             project_folder(test_root()), '''{
             "project_name": "project1",
             "roles_seq": ["main"],
             "predefined_variables": {
               "name1": "aa bb",
               "name2": "bb"
              }
}

''')

@with_setup(setup_deploy, remove_test_folder)
def test_config():
    project_path = "project1"
    config_name = "dev"
    
    deploy_config(project_path, config_name)

    assert_that(contents_of(os.path.join(test_root(), project_path, "deploy", "." + config_name, "main.host"))) \
    .contains("[all:vars]") \
    .contains('name1 = aa bb') \
    .contains('name2 = bb') \
    .contains('name3 = c') \
    .contains('1.1.1.1')
