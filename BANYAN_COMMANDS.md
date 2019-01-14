# Sub Commands
- [init](#init)
- [build](#build)
- [config](#config)
- [get](#get)
- [clear](#clear)
- [deploy](#deploy)

All the commands should run at the root of the workspace. Please refer to the [banyan specifications](SPEC.md)
## init
Initialize the file for banyan configuration.
```
banyan init -p project1 -c dev
```
Then the `dev.cfg` file will be found at `.workspace/project1/deploy/dev.cfg`

## build
Build the all of the ansible scripts.
```
banyan build -p project1 -c dev
```
This process will take two effects:
1. Generate the structure and files for ansible script.
2. Gather all variables together with values from all of the defaults section of the roles and write them to `predefined_variables` node of `dev.cfg`.

### Build without modifying the configuration
If you want to skip the second effect, please run the following command.
```
banyan build -p project1 -c dev --only-structure=True
```

### Build for remote deployment
The above instructions are for local environment. If you want to build the script for remote environment, please follow the command below.
```
banyan build -p project1 -c dev -r 10.0.0.1 -k ./remote_key -n remote_login
```

### Build authentication layer
The autentication layer is designed to protect your microservices. This is useful when you expose your microservices to a none private environment. Of course, when you develop your microservice, you don't need it.
```
banyan build -p project1 -c dev --build-gate=True
```

## config
Configure the inventory items
```
banyan config -p project1 -c dev
```
In the build process, you get the all of the default variables and values defined in the defaults of the roles. You may configure them with different value based on the environment. When you run this command, it reflects the changes in the `dev.cfg` to `main.host`.

## clear
```
banyan clear -p project1 -c dev
```
It removes the generated `.dev` folder. Then you can run `build` again for changes

## get
```
banyan get --giturl=https://***.git --tag="v0.1.1" -c dev -k "key_file"
```
In the init process, it downloads the `v0.1.1` from git and then download the other depended projects with the configuration in `dev.cfg`. 

## deploy
```
banyan deploy -p project1 -c dev
```
The final step is `deploy` which make the microservices run in local development or remote production servers.
