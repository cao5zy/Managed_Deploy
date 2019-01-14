import os
from assertpy import assert_that
from codegenhelper import test_root, init_test_folder, remove_test_folder
from ..util import init_root, get_project_path
from nose import with_setup
from ..debug import simple as debug_simple
from ..roles import link as roles_link, load as roles_load
from .setup_roles_data import setup_roles_files, setup_roles_folder

init_root(test_root())

@with_setup(setup_roles_files, remove_test_folder)
def test_get_roles():
    roleobjs = debug_simple(roles_load(os.path.join(test_root(), "project1", "deploy", "dev.cfg")))
    
    assert_that(roleobjs).is_length(3)
    assert_that(roleobjs[0]).contains_entry({"name": "project2_main"}, {"local": get_project_path("project2")})
    assert_that(roleobjs[len(roleobjs) - 1]).contains_entry({"name": "project1_test"}, {"local": get_project_path("project1")})



@with_setup(setup_roles_folder, remove_test_folder)
def test_link_rols():
    roles_data = roles_load(os.path.join(test_root(), "project1", "deploy", "dev.cfg"))
    roles_link(roles_data, os.path.join(test_root(), "project1", "deploy"))

    assert_that(".test/project1/deploy/roles/project1_main").exists()
    assert_that(".test/project1/deploy/roles/project1_test").exists()
    assert_that(".test/project1/deploy/roles/project2_main").exists()
    assert_that(os.path.islink(".test/project1/deploy/roles/project1_main")).is_true()
    assert_that(os.path.islink(".test/project1/deploy/roles/project1_test")).is_true()
    assert_that(os.path.islink(".test/project1/deploy/roles/project2_main")).is_true()
 
  
