#!/usr/bin/env python
from setuptools import setup, find_packages
name = "mc_banyan"

requires = ['demjson>=2.2.4', 'jinja2>=2.10', 'pyyaml>=3.13', 'shell>=1.0.1', 'codegenhelper>=0.0.13', 'fn', 'md_codegen>=0.5.0']

setup(
    name = name,
    version = '2.1.0',
    scripts = ["scripts/banyan"],
    author = 'Zongying Cao',
    author_email = 'zongying.cao@dxc.com',
    description = 'banyan is a tool to manage the deployment tasks for microservices.',
    long_description = """banyan is a tool to manage the deployment tasks for microservices.""",
    packages = [name],
    package_dir = {'mc_banyan': 'src'},
    package_data = {'mc_banyan': ["*.py", "*.t"]},
    include_package_data = True,
    install_requires = requires,
    license = 'Apache',
    classifiers = [
               'Development Status :: 4 - Beta',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development :: Libraries',
           ],
)
