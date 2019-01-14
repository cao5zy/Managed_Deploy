from assertpy import assert_that
from ...githelper import get_tag
from codegenhelper import init_test_folder, remove_test_folder, test_root
from nose import with_setup
import os

def setup_get():
    init_test_folder()

@with_setup(setup_get, remove_test_folder)
def test_get():
    project_name = "banyan"
    giturl = "https://github.com/cao5zy/banyan"
    tag = "v0.0.3"
    location = test_root()
    get_tag(giturl, tag, location=location)

    assert_that(os.path.join(test_root(), "banyan")).exists()

@with_setup(setup_get, remove_test_folder)
def test_get_from_private_repo():
    project_name = "codegen"
    giturl = "git@github.dxc.com:zcao2/codegen.git"
    tag = "v0.2.7"
    location = test_root()
    get_tag(giturl, tag, location=location)

    assert_that(os.path.join(test_root(), "codegen")).exists()

