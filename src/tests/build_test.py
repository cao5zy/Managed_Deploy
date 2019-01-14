from nose import with_setup
from codegenhelper import init_test_folder, remove_test_folder, test_root, debug, put_folder, put_file
from fn import F, _
import os
from assertpy import assert_that, contents_of
from ..deploy import build_deploy_script
import demjson
from ..util import init_root, get_deploy_host, get_deploy_yml, get_deploy_ansible_cfg_path
import logging

logging.basicConfig(level=logging.DEBUG)

init_root(test_root())

def setup_build():
    init_test_folder()
    init_root(test_root())
    project_folder = F(put_folder, "project1") >> F(put_folder, "deploy")
    put_file("main.yml", \
             (project_folder >> F(put_folder, "roles") >> F(put_folder, "main") >> F(put_folder, "defaults"))(test_root()),\
             '''---
name1: "a"
name2: "b"
...
 ''')
    put_file("dev.cfg", \
             project_folder(test_root()), '''{
             "project_name": "project1",
  "roles_seq": ["main"]
}

''')


@with_setup(setup_build, remove_test_folder)
def test_build():
    assert_that(os.path.join(test_root(), "project1", "deploy", "roles", "main", "defaults", "main.yml")).exists()
    build_deploy_script("project1", "dev")
    assert_that(demjson.decode_file(os.path.join(test_root(), "project1", "deploy", "dev.cfg"))["predefined_variables"]).contains_entry({"name1": "a"}, {"name2": "b"})    

@with_setup(setup_build, remove_test_folder)
def test_only_build_structure():
    build_deploy_script("project1", "dev", only_structure=True)
    assert_that("predefined_variables" not in demjson.decode_file(os.path.join(test_root(), "project1", "deploy", "dev.cfg"))).is_true()
    
@with_setup(setup_build, remove_test_folder)
def test_build_remote():
    build_deploy_script("project1", "dev", remote_dict = {"key": "./remote_key", "remote_user": "alan", "remote_addr": "10.0.0.9"})
    assert_that(contents_of(get_deploy_host("project1", "dev"))).contains("[remote]\n") \
    .contains("10.0.0.9")
    assert_that(contents_of(get_deploy_yml("project1", "dev"))).contains("hosts: remote")

    assert_that(get_deploy_ansible_cfg_path("project1", "dev")).exists()
    assert_that(contents_of(get_deploy_ansible_cfg_path("project1", "dev")))\
        .contains("[defaults]\n") \
        .contains("remote_user=alan") \
        .contains("private_key_file=./remote_key") \
        .contains("host_key_checking=False")
