# Banyan configuration #

Banyan configuration tells the banyan program how to group the roles together and generate the script for you.   
The structure of the file is as following.  
```
{
    "project_name": "name of the project",
    "dependencies": [{
        "project_name": "<project name>",
	"giturl": "<git url>",
	"tag": "<git tag>",
	"config_name": "<configuration name>"
    }],
    "roles_seq": ["role1", "role2"],
    "predefined_variables": {
        "host": "130.71.32.2"
    }
}

```
* project_name  
The name of the project.    
>Please refer to [banyan sepecifications](init-from-remote/SPEC.md) for more details about the folder structure.   
* dependencies  
The `dependencies` tells banyan program what projects are depended and where to get them. It will load the depended project recursively until meet the project that doesn't have dependencies.   
* roles_seq
The `roles_seq` tells banyan program the sequence of managing roles.  
* predefined_variales  
The `predefined_variables` stores the values for the current deployment case. 

