from src.tools.data_convert import dict2yml
from assertpy import assert_that

def test_dict2yml():
    
    def test(result):
        assert_that(result).contains('''name: "alan"''').contains('''port: 323''')

    test(dict2yml({"name": "alan", "port": 323}))
