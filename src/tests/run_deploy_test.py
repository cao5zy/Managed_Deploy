import os
from src.deploy import run_deploy
from assertpy import assert_that
from nose import with_setup
from codegenhelper import test_root as root_folder, init_test_folder as init_folder, remove_temp_folder as remove_folder, put_folder as create_folder, put_file as create_file

folder_name = "folder1"
bash_file = "main.sh"
test_file = "test.txt"

def setup_run_deploy():
    init_folder()
    create_file(test_file, create_folder(folder_name, root_folder()), '''hello
''')
    create_file(bash_file, create_folder(folder_name, root_folder()), '''rm ./test.txt
''')

@with_setup(setup_run_deploy, remove_folder)
def test_run_deploy():
    curr_dir = os.getcwd()
    assert_that(os.path.exists(os.path.join(root_folder(), folder_name, test_file))).is_true()
    run_deploy(os.path.join(root_folder(), folder_name))
    assert_that(os.path.exists(os.path.join(root_folder(), folder_name, test_file))).is_false()
    assert_that(os.getcwd()).is_equal_to(curr_dir)
