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
Build all of the ansible scripts.
```
banyan build -p project1 -c dev
```
This process will take two effects:
1. Generate the structure and files for ansible script.
2. Gather all variables together with values from all of the defaults section of the roles and write them to `predefined_variables` node of `dev.cfg`.

### Build without modifying the configuration
If you want to skip the second effect, please run the following command.
```
banyan build -p project1 -c dev --only-structure
```

### Build for remote deployment
The above instructions are for local environment. If you want to build the script for remote environment, please follow the command below.
```
banyan build -p project1 -c dev -r 10.0.0.1 -k ./remote_key -n remote_login
```

### Build authentication layer
The autentication layer is designed to protect your microservices. This is useful when you expose your microservices to a none private environment. Of course, when you develop your microservice, you don't need it.
```
banyan build -p project1 -c dev --build-gate
```
This command will put all of the microservices behind the authentication layer. But sometimes, it is required to get some microservcies public. 
```
banyan build -p project1 -c dev --build-gate --noauth=project2
```
This command will make project2 accessed without authentication.

### Build for customized proxy mapping
Currently, the proxy mapping is default to the microservice project name. There is a way to let you control the proxy mapping.

To explain it clearly, here is a exmaple.  
The structure of microservice projects.
```
workspace
  |-project1
  |-project2
```
The build command with default proxy mapping is as following.   
```
banyan build -p project1 -c dev --build-gate
```
The output of the proxy mapping is as following.
```
location /_api/project1/ {
    ...
}

location /_api/project2/ {
    ...
}

```

Now, we want to set the proxy mapping for `project1` as `/project1/`. The command would go as following.   
```
banyan build -p project1 -c dev --build-gate --proxy-mapping=project1:/project1/
```
The output of the proxy mapping is as following.
```
location /_api/project2/ {
    ...
}

location /project1/ {
    ...
}

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

### deploy the specified roles
Sometimes, especially when you develop your microservice with other microservices, you would expect to deploy your own microservice container instead all microservices. The subcommand `--role-tags` can help.
```
banyan deploy -p project1 -c dev --role-tags="project1_main"
```
