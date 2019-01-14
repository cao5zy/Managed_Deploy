import os
from nose import with_setup
import traceback
from assertpy import assert_that, contents_of
import time
from codegenhelper import test_root, init_test_folder, remove_test_folder, put_folder, put_file
from ..defaults import all as defaults_all, override_values as defaults_override_values, write as defaults_write
from ..init_config import init_config
from fn import F
import demjson
from ..util import get_config_path, init_root

init_root(test_root())


def setup_init_config():
    init_test_folder()
    (F(put_folder, "abc") >> \
        F(put_folder, "deploy") >> \
        F(put_folder, "roles") >> \
        F(put_folder, "role1"))(test_root())

    (F(put_folder, "abc") >> \
        F(put_folder, "deploy") >> \
        F(put_folder, "roles") >> \
        F(put_folder, "role2"))(test_root())
    
    
@with_setup(setup_init_config, remove_test_folder)
def test_init_config():
    project_name = "abc"
    config_name = "dev"
    init_config(project_name, config_name)

    json = demjson.decode_file(get_config_path(project_name, config_name))

    assert_that(json).contains_entry({"project_name": "abc"}) \
        .contains_entry({"predefined_variables": {}})

    assert_that(json["roles_seq"]).contains("role1", "role2")
    
    assert_that(json["dependencies"][0]).contains_entry({"project_name": "<project_name>"}) \
        .contains_entry({"git": "<git_url>"}) \
        .contains_entry({"config_name": "<configuration_name>"})



