import os
import shutil
from nose import with_setup
import traceback
from assertpy import assert_that, contents_of
import time
from codegenhelper import test_root, init_test_folder, remove_test_folder, put_folder, put_file
from ..defaults import all as defaults_all, override_values as defaults_override_values, write as defaults_write
from ..util import init_root

init_root(test_root())

def setup_single_role():
    init_test_folder()
    put_file("main.yml", put_folder("defaults", put_folder("project1_main", put_folder("roles", test_root()))), '''
name1: x
name2: y
''')

def teardown_func():
    remove_test_folder()
    

def setup_muti_role_with_duplicated_key():
    init_test_folder()

    put_file("main.yml", put_folder("defaults", put_folder("project1_role1", put_folder("roles", test_root()))), '''
name1: y
name2: x
''')
    put_file("main.yml", put_folder("defaults", put_folder("project2_role2", put_folder("roles", test_root()))), '''
name1: y
name3: x
''')

def setup_multi_role():
    init_test_folder()

    put_file("main.yml", put_folder("defaults", put_folder("project1_role1", put_folder("roles", test_root()))), '''
name1: y
name2: x
''')
    put_file("main.yml", put_folder("defaults", put_folder("project2_role2", put_folder("roles", test_root()))), '''
name4: y
name3: x
''')

@with_setup(setup_single_role)
def test_get_defaults():
    assert_that(defaults_all(test_root())).contains_entry({"name1":"x"}, {"name2":"y"})


@with_setup(setup_muti_role_with_duplicated_key, teardown_func)
def test_get_defaults_with_duplicated_keys():
    # assert_that(defaults_all).raises(Exception).when_called_with(test_root())
    pass
@with_setup(init_test_folder, teardown_func)
def test_write():
    import yaml

    def test_func(file_path):
        defaults_write(file_path, {"name1": "x1", "name2": "x2", "age": 5})

        def test(contents):
            assert_that(contents).contains('''name1=x1''') \
                                 .contains('''name2=x2''') \
                                 .contains('''age=5''')
        
        test(contents_of(file_path))

    test_func(os.path.join(test_root(), "hosts"))
    
    
@with_setup(setup_multi_role, teardown_func)
def test_get_defaults_with_role_names():
    def test(results):
        assert_that(results).contains_entry({"name1":"y"}, {"name2":"x"})
        assert_that(results).does_not_contain_key("nam3", "name4")

    test(defaults_all(test_root(), ["project1_role1"]))

    
def test_override_values():
    def test(result):
        assert_that(result) \
            .contains_entry({"host": "192.168.1.1"}) \
            .contains_entry({"port": 8080}) \
            .contains_entry({"container_name": "abc"}) \
            .contains_entry({"login": "bcd"})
    
    test(defaults_override_values({
        "project_name": "project1",
        "predefined_variables": {
            "host": "192.168.1.1",
            "port": 8080,
            "container_name": "abc"
        }
    }, {
        "host": "0.0.0.0",
        "port": 80,
        "login": "bcd"
    }))
