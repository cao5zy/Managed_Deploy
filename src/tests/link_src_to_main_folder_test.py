import os
from assertpy import assert_that
from codegenhelper import put_folder, test_root as root_folder, put_file, remove_temp_folder
from ..util import init_root
from nose import with_setup
from ..debug import simple as debug_simple
from ..roles import link as roles_link, load as roles_load, link_src_to_deploy
from .setup_roles_data import setup_roles_folder

init_root(root_folder())

@with_setup(setup_roles_folder, remove_temp_folder)
def test_getlink_src_to_deploy():
    link_src_to_deploy(debug_simple(roles_load(os.path.join(root_folder(), "project1", "deploy", "dev.cfg")), "roles"))

    assert_that(os.path.join(root_folder(), "project1", "deploy", "roles", "main", "files", "src", "index.js")).exists()
