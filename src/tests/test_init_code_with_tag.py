from ..get_code_with_tag import init_tag_for_project
import os
from codegenhelper import test_root as root_folder, init_test_folder as init_folder, remove_temp_folder as remove_folder, put_folder as create_folder, put_file as create_file
from assertpy import assert_that
from nose import with_setup

def setup_init_tag_for_project():
    init_folder()

@with_setup(setup_init_tag_for_project, remove_folder)
def test_init_tag_for_project():
    giturl = "https://github.com/cao5zy/alan_cao_test"
    tag = "0.0.1"
    config_name = "app"
    
    init_tag_for_project(giturl, tag, config_name, os.path.join(root_folder()))

    assert_that(os.path.join(root_folder(), "alan_cao_test")).exists()
    assert_that(os.path.join(root_folder(), "alan_cao_test1")).exists()
    assert_that(os.path.join(root_folder(), "alan_cao_test2")).exists()
