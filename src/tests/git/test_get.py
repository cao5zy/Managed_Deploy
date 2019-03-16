from assertpy import assert_that
from ...githelper import get_tag
from codegenhelper import init_test_folder, remove_test_folder, test_root
from nose import with_setup
import os

def setup_get():
    init_test_folder()

@with_setup(setup_get, remove_test_folder)
def test_get():
    giturl = "https://github.com/cao5zy/testrepo"
    tag = "v0.0.1"
    location = test_root()
    get_tag(giturl, tag, location=location)

    assert_that(os.path.join(test_root(), "testrepo")).exists()

@with_setup(setup_get, remove_test_folder)
def test_get_from_private_repo():
    giturl = "git@github.com:cao5zy/test_private_repo.git"
    tag = "v1.0.0"
    location = test_root()
    get_tag(giturl, tag, location=location)

    assert_that(os.path.join(test_root(), "test_private_repo")).exists()

