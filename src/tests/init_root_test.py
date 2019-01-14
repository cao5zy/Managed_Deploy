import os
import shutil
from nose import with_setup
import traceback
from assertpy import assert_that, contents_of
import time
from codegenhelper import test_root, init_test_folder, remove_test_folder, put_folder, put_file
from ..defaults import all as defaults_all, override_values as defaults_override_values, write as defaults_write, init_root

def setup_single_role():
    init_test_folder()
    put_file("main.yml", put_folder("defaults", put_folder("main", put_folder("roles"))), '''
name1: x
name2: y
''')

def teardown_func():
    remove_test_folder()
    

def setup_muti_role_with_duplicated_key():
    init_test_folder()

    put_file("main.yml", put_folder("defaults", put_folder("role1", put_folder("roles", test_root()))), '''
name1: y
name2: x
''')
    put_file("main.yml", put_folder("defaults", put_folder("role2", put_folder("roles", test_root()))), '''
name1: y
name3: x
''')

def test_init_root():
    values = {
        "project_name": "alan",
        "folder_root": "home/caozon/mic/abc"
    }
    project_name = "abc"
    assert_that(init_root(project_name + "_main", values)).contains_entry({"project_name": "alan"}).contains_entry({"folder_root": os.path.join(os.getcwd(), project_name)})


