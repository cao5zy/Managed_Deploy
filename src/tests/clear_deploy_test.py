from nose import with_setup
from codegenhelper import init_test_folder, remove_test_folder, test_root, debug, put_folder
from fn import F, _
import os
from assertpy import assert_that
from ..clear_deploy import clear_deploy

def setup_clear_deploy():
    init_test_folder()
    f = F(put_folder, ".dev") << F(put_folder, "deploy") << F(put_folder, "project1")
    f(test_root())
    
@with_setup(setup_clear_deploy, remove_test_folder)
def test_clear_deploy():
    
    assert_that(os.path.join(test_root(), "project1", "deploy", ".dev")).exists()

    clear_deploy(os.path.join(test_root(), "project1"), "dev")
    assert_that(os.path.exists(os.path.join(test_root(), "project1", "deploy", ".dev"))).is_false()
