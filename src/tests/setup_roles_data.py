from codegenhelper import test_root, init_test_folder, put_folder, put_file

def setup_roles_files():
    init_test_folder()

    put_file("dev.cfg", put_folder("deploy", put_folder("project1", test_root())), '''
{
    "project_name":"name1",
    "dependencies":[
        {"project_name": "project2"}
    ],
    "roles_seq":["main", "test"]
}
    ''')

    put_file("index.js", put_folder("src", put_folder("project1", test_root())), '''//for test only''')


    put_file("dev.cfg", put_folder("deploy", put_folder("project2", test_root())), '''
{
    "project_name":"name2",
    "roles_seq":["main"]
}
''')

def setup_roles_folder():
    setup_roles_files()

    put_folder("main", put_folder("roles", put_folder("deploy", put_folder("project1", test_root()))))
    put_folder("test", put_folder("roles", put_folder("deploy", put_folder("project1", test_root()))))
    put_folder("main", put_folder("roles", put_folder("deploy", put_folder("project2", test_root()))))
