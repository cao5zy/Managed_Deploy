from ..gate import build_gate
from assertpy import assert_that
from nose import with_setup
from codegenhelper import test_root, init_test_folder, remove_test_folder, put_folder, put_file
import os
import logging
from ..util import init_root
import demjson

logging.basicConfig(level=logging.DEBUG)

project_name = "inventory_service"
config_name = "dev"

init_test_folder()
def init_test_build_gate():
    put_file('dev.cfg', put_folder('deploy', put_folder('inventory_service', test_root())), '''
{
    "project_name": "inventory_service",
    "roles_seq": ["main"]
}
''')
    put_file('main.yml', put_folder('tasks', put_folder('roles', put_folder('deploy', put_folder('inventory_service', test_root())))), '''
---
-name: hello from main
...
''')

@with_setup(init_test_build_gate, remove_test_folder)
def test_build_gate():
    try:
        init_root(test_root())
        build_gate(project_name, config_name, True)
    finally:
        init_root(os.getcwd())

    print('test_build_gate')
    print(os.listdir('./'))
    print(os.listdir(os.path.join(test_root())))
    print(os.listdir(os.path.join(test_root(), project_name)))
    print(os.listdir(os.path.join(test_root(), project_name, "deploy")))
    print(os.listdir(os.path.join(test_root(), project_name, "deploy", "roles")))
    
    assert_that(os.path.join(test_root(), project_name, "deploy", "roles", "auth_db")).exists()
    assert_that(os.path.join(test_root(), project_name, "deploy", "roles", "microservice_gate")).exists()

    config = demjson.decode_file(os.path.join(test_root(), project_name, "deploy", "dev.cfg"))
    assert_that(config["roles_seq"]).contains("auth_db").contains("microservice_gate")
