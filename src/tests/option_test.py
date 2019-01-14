from assertpy import assert_that
from ..banyan_opt import get_options

def test_get_options():
    assert_that(get_options(['banyan', 'deploy', '-p', 'project1', '-c', 'banyan']))\
        .has_projectname("project1")\
        .has_cfg("banyan")\
        .has_command("deploy")

def test_get_only_structure_option():
    assert_that(get_options(['banyan', 'deploy', '-p', 'project1', '-c', 'banyan', '-s', 'True']))\
        .has_projectname("project1")\
        .has_cfg("banyan")\
        .has_command("deploy")\
        .has_only_structure(True)
    
