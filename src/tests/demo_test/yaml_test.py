import yaml
from assertpy import assert_that
import debug

def test_load_yaml_dict_str():
    def test(data):
        assert_that(data).contains_entry({"name": "abc"}, {"key": "bcd"})

    test(yaml.load(debug.simple('''name: "abc"
key: "bcd"''', "test_load_yaml_dict_str")))
