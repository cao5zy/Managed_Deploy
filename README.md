# banyan #
Banyan is a microservice deployment management tool. It assumes that your microservice projects deployment are driven by ansible. If you are interesting in it, please make sure your project development is compliant to the [specifications](SPEC.md) and [banyan configuration](BANYAN_CFG.md).

# Background  
The banyan program assumes that the project subjects to [specifications](SPEC.md). Based on [specifications](SPEC.md), the depended project should be in the same folder.   

# How to use it
## Installation
```
/usr/bin/python3 -m pip install mc_banyan
```
`banyan` is developed in python 3.x. Please make sure python 3.x has been installed in your system.   

---
There are two cases to work with `banyan`.   
## Deployment case 
```
mkdir working_space
cd working_space
banyan get -u <git-url> -c <configuration-name>
```
Please refer to [banyan commands:get](BANYAN_COMMANDS.md#get) for more details.

In the deployment case, all of the configurations are available. So you should to following steps to finish deployment.
1. `banyan get -u https://...entry_project.git -c dev -t v1.1.0` 
  * It download code of project from the tag `v1.1.0`
  * It downloads other code of project defined in `dependencies` in dev.cfg
2. `banyan build -p entry_project -c dev --only-structure=True -n alan_cao -r 10.10.1.1 -k ./remote_key`
  * It builds the deployment folder `.dev` and all necessary files for ansible playbook
  * The ssh private key file for remote access should be placed under `.dev` folder based on `-k ./remote_key`
3. `banyan config -p entry_project -c dev`
  * Set the variables in `.dev/main.host` based on the values in `dev.cfg`
4. `banyan deploy -p entry_project -c dev`
  * Deploy the microservices to `10.10.1.1`
5. `banyan clear -p entry_project -c dev`
  * Remove the `.dev` folder if you don't want your `ansible.cfg` be revealed.


## Development case
```
mkdir workspace
cd workspace
```
1. The developer should mannually create the microservice projects under `workspace` folder.
2. `banyan init -p project1 -c dev`
  * The developer should create the `banyan` configuration file to build the relationships between the microservices.
3. `banyan build -p project1 -c dev`
  * The command collects all of the variables defined in defaults in roles into the `predefined_variables` in `dev.cfg`
  * The developer should set the values in `predefined_variables` based on environment, ie, the port number and prefix.
  * soft link the `src` folder to `deploy/roles/main/files/src`. In that case, the ansible modules can work on the source code directly without predefine the path of the source code. 
4. `banyan config -p project1 -c dev`
  * The command writes the values in `predefined_variables` into `.dev/main.host`
5. `banyan deploy -p project1 -c dev`
  * The command deploy the microservices and run them in your local

If the microservice projects are cloned to your local, the #3 step should be .
```
banyan build -p project1 -c dev --only-structure=True
```

After the command executing, the generated folder structure would be like following. 
```
working_space
|-project1
|-src
|-deploy
  |-dev.cfg
  |-.dev
    |-main.host
    |-main.yml
    |-main.sh
    |-roles
      |-role-folders 
      |- ...
```

