import os
import demjson
from assertpy import assert_that
from codegenhelper import test_root as root_folder, init_test_folder as init_folder, remove_temp_folder as remove_folder, put_folder as create_folder, put_file as create_file
from ..config import is_db_role

def test_is_db_role():
    assert_that(is_db_role({'role_name': 'auth-db'})).is_true()
    assert_that(is_db_role({'role_name': 'auth_service'})).is_false()
