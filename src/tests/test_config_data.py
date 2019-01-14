from ..config import load_all_dependencies
from codegenhelper import test_root as root_folder, init_test_folder as init_folder, remove_temp_folder as remove_folder, put_folder as create_folder, put_file as create_file
from nose import with_setup
import os
import demjson
from assertpy import assert_that

def setup_load_all_dependencies():
    init_folder()

    create_file("app.cfg", create_folder("deploy", create_folder("app", root_folder())), '''{
    "project_name": "app",
    "dependencies": [{
        "project_name": "app1",
        "config_name": "app1"
}
]
}''')
    create_file("app1.cfg", create_folder("deploy", create_folder("app1", root_folder())), '''{
    "project_name": "app1",
    "dependencies": [{
        "project_name": "app2",
        "config_name": "app2"
}
]

}''')
    create_file("app2.cfg", create_folder("deploy", create_folder("app2", root_folder())), '''{
    "project_name": "app2",
    "dependencies": [{
        "project_name": "app3",
        "config_name": "app3"
}
]

}''')
    create_file("app3.cfg", create_folder("deploy", create_folder("app3", root_folder())), '''{
    "project_name": "app3"
}''')

    

@with_setup(setup_load_all_dependencies, remove_folder)
def test_load_all_dependencies():
    config_path = os.path.join(root_folder(), "app", "deploy", "app.cfg")
    deps = []
    def handler(dep_config):
        deps.append(dep_config["project_name"])
        return demjson.decode_file(os.path.join(root_folder(), dep_config["project_name"], "deploy", dep_config["config_name"] + ".cfg"))
                                   
    load_all_dependencies(config_path, handler)

    assert_that(deps).contains("app1").contains("app2").contains("app3")
