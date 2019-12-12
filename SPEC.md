# Banyan specifications #

# Project structure  
```
work_space
  |- project_folder1
    |- *
  |- project_foler2
    |- *
  |- project_folder
    |-src
      |-code_file_1
      |-code_file_2
      |-code_file_n
    |-deploy
      |-banyan.cfg
      |-*.cfg
      |-roles
        |-role1
            |-defaults
                |-main.yml
            |-vars
                |-main.yml
            |-tasks
                |-main.yml
```
There should be a folder as a root folder to hold all folders of microservices.

* project_folder  
The `project_folder` is the place to hold the microservice project.
* src  
The `src` is the place to hold the source of the microservice project
* deploy  
The `deploy` is the place to hold configurations and ansible scripts. 
You can have multiple [banyan configuration files](BANYAN_CFG.md) in `deploy` folder for different deployment plans.  
* roles  
The `roles` is the place to hold [ansible roles](http://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html).  
* defaults  
The `defaults` folder holds the variables that would be overriden in the integration. 
* banyan.cfg  
`banyan.cfg` is the default configuration.
* *.cfg  
`*.cfg` are files to hold the configurations for different cases.

