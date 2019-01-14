from optparse import OptionParser
import sys
from .debug import simple as debug_simple

opt_configs = [
{
    "short": "p",
    "long": "projectname",
    "dest": "projectname",
    "help": "the project name"
},
    {
        "short": "c",
        "long": "cfg",
        "dest": "cfg",
        "help": "the banyan configuration file name",
        "default": "dev"
    },
    {
        "short": "u",
        "long": "giturl",
        "dest": "giturl",
        "help": "git url for the project",
        "default": None
    },
    {
        "short": "t",
        "long": "tag",
        "dest": "tag",
        "help": "tag of the project",
        "default": "v1.0.0"
    },
    {
        "short": "s",
        "long": "only-structure",
        "dest": "only_structure",
        "help": "only build the structure",
        "default": "False"
    },
    {
        "short": "k",
        "long": "key-file",
        "dest": "key_file",
        "help": "private key file for accessing the remote",
        "default": None
    },
    {
        "short": "r",
        "long": "remote-addr",
        "dest": "remote_addr",
        "help": "remote address",
        "default": None
    },
    {
        "short": "n",
        "long": "user-name",
        "dest": "user_name",
        "help": "user name of the remote",
        "default": None
    },
    {
        "short": "g",
        "long": "build-gate",
        "dest": "build_gate",
        "help": "default is false to not build the gate",
        "default": False
    },
    {
        "short": "o",
        "long": "role-tags",
        "dest": "role_tags",
        "help": "specify role tags to only run the roles",
        "default": None
    }
]
def get_options(sys_args = None):

    def configure_parser(parser):
        def add_opt(opt):
            parser.add_option("-"+opt["short"], \
                              "--" + opt["long"], \
                              dest=opt["dest"] if "dest" in opt else None, \
                              help=opt["help"] if "help" in opt else None, \
                              default = opt["default"] if "default" in opt else None)

        [add_opt(opt) for opt in opt_configs]
        
        (options, args) = parser.parse_args(debug_simple(sys_args or sys.argv, "original args"))

        class dumy:
            def __init__(self):
                self.projectname = options.projectname
                self.cfg = options.cfg
                self.command = args[1]
                self.giturl = options.giturl
                self.tag = options.tag
                self.only_structure = options.only_structure.strip().lower() == 'true'
                self.key_file = options.key_file
                self.remote_addr = options.remote_addr
                self.user_name = options.user_name
                self.build_gate = options.build_gate == True or (isinstance(options.build_gate, str) and  options.build_gate.lower() == "true")
                self.role_tags = None if options.role_tags == None else options.role_tags.split(',')
        return dumy()

    return configure_parser(OptionParser())
