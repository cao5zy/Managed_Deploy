from ..gate import build_gate
from assertpy import assert_that, contents_of
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

def init_test_build_gate_with_authorization():
    put_file('dev.cfg', put_folder('deploy', put_folder('inventory_service', test_root())), '''
{
    "project_name": "inventory_service",
    "dependencies": [{
      "project_name": "inventory_service_authorization",
      "config_name": "dev"
     }],
    "roles_seq": ["main"]
}
''')
    put_file('main.yml', put_folder('tasks', put_folder('roles', put_folder('deploy', put_folder('inventory_service', test_root())))), '''
---
-name: hello from main
...
''')
    
    put_file('dev.cfg', put_folder('deploy', put_folder('inventory_service_authorization', test_root())), '''
{
    "project_name": "inventory_service_authorization",
    "roles_seq": ["main"]
}
''')
    assert_that(os.path.join(test_root(), "inventory_service_authorization", "deploy", "dev.cfg")).exists()
    put_file('main.yml', put_folder('tasks', put_folder('roles', put_folder('deploy', put_folder('inventory_service_authorization', test_root())))), '''
---
-name: hello from main
...
''')
    assert_that(os.path.join(test_root(), "inventory_service_authorization", "deploy", "roles", "tasks", "main.yml")).exists()



@with_setup(init_test_build_gate, remove_test_folder)
def test_build_gate():
    try:
        init_root(test_root())
        build_gate(project_name, config_name, True)
    finally:
        init_root(os.getcwd())

    assert_that(os.path.join(test_root(), project_name, "deploy", "roles", "auth_db")).exists()
    assert_that(os.path.join(test_root(), project_name, "deploy", "roles", "microservice_gate")).exists()

    config = demjson.decode_file(os.path.join(test_root(), project_name, "deploy", "dev.cfg"))
    assert_that(config["roles_seq"]).contains("auth_db").contains("microservice_gate")

@with_setup(init_test_build_gate, remove_test_folder)
def test_build_gate_with_proxy_mapping():
    try:
        init_root(test_root())
        build_gate(project_name, config_name, True, "inventory_service:/")
    finally:
        init_root(os.getcwd())

    yml_content = contents_of(os.path.join(test_root(), project_name, "deploy", "roles", "microservice_gate", "templates", "login.conf.template"))

    assert_that(yml_content).contains('location / {') \
        .contains('http://inventory_service/;')

@with_setup(init_test_build_gate, remove_test_folder)
def test_build_gate_with_no_auth():
    try:
        init_root(test_root())
        build_gate(project_name, config_name, True, "inventory_service:/", "inventory_service")
    finally:
        init_root(os.getcwd())

    yml_content = contents_of(os.path.join(test_root(), project_name, "deploy", "roles", "microservice_gate", "templates", "login.conf.template"))

    assert_that(yml_content.replace(os.linesep, '')).does_not_contain('location / {\tresolver	{{auth_db_ip}} valid=30s')

@with_setup(init_test_build_gate_with_authorization, remove_test_folder)
def test_build_gate_with_authorization():
    try:
        init_root(test_root())
        build_gate(project_name, config_name, True, authorization="inventory_service_authorization")
    finally:
        init_root(os.getcwd())

    def dumy(config_path):
        assert_that(config_path).exists()
        yml_content = contents_of(config_path)
        assert_that(yml_content).does_not_contain('"inventory_service"')
        
    dumy(os.path.join(test_root(), project_name, "deploy", "roles", "microservice_gate", "templates", "login.conf.template"))
