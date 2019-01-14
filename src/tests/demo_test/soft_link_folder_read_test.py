from codegenhelper import test_root, init_test_folder, remove_test_folder, put_folder, put_file
from src import debug
from nose import with_setup
import os
from assertpy import assert_that

debug.on()

def setup_test_folder():
    init_test_folder()
    def create(root_folder):
        put_file("level3_file", put_folder("level3", put_folder("level2", root_folder)), "hello level3_file")
        os.symlink(os.path.join(os.path.abspath(root_folder), "level2", "level3"), os.path.join(os.path.abspath(root_folder), "link_to_level2"))

    create(put_folder("level1", test_root()))
    
@with_setup(setup_test_folder, remove_test_folder)
def test_read_sub_folders_from_link():
    def test(result):
        assert_that(result).contains_duplicates()
        assert_that(list(filter(lambda x:x.find("level3_file") != -1, result))).is_length(2)

    test([y for x in [debug.simple(files, "test_read_sub_folders_from_link") for _,_,files in os.walk(test_root(), followlinks = True)] for y in x])
