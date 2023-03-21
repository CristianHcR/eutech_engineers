# **Automate User Account Creation Script**

## **Objective**

The objective for this task it's create a script on python to create multiple users on linux this script will must contain the username, password user, home directory and shell.

## **Materials**

For do this task we will need:

- Python installed, in this case **"python 3.10"** 
-  S.O Linux, in this case **"ubuntu 20.04"**

## **INDEX** 
+ [Develoment](#development)
  + [1. Configuration File](#1-create-the-configuration-json-file)
    + [1.1  (OPTIONAL FILE)](#11-optional-configuration-file-b)
  + [2.]()

+ [Comprobations]
+ [Create User Script](/task2/create_user/)
+ [(Optional) Delete User Script](/task2/remove_user/)

## **Development**

## **1. Create the configuration json file**

First of all, we will create a .json file in this case "config.json" to create users:

![](img/01.png)

  
- **Explanations**

    And this will contain:

    - **"users"** : This key will contain all the users that will be created. It is likely that the value of this key will be a list or an array that will hold all the user objects, each with their own set of properties such as "username", "password", etc.

    > **Example**:
    >
    >```
    >{
    >   users:[
    >       {
    >         "username":...,
    >          "password":...
    >       }
    >    ]
    >}
    >```



    - **"username"**: This key will define the username to be created for a user. The value of this key will be a string that specifies the username.

    > **Example:**
    > ```  
    >{ ...
    >
    >   "username": "example"
    >    ...
    >}
    > ```
    - **"password":** This key will define the password of the user. The value of this key will be a string that specifies the password. It is **important** to note that passwords should always be stored in an encrypted form to maintain security.

    > **Example:**
    > ```  
    >{ ...
    >
    >   "password": "pass123"
    >    ...
    >}
    > ```

    - **"shell"**: This key will define which shell the user will use. The value of this key will be a string that specifies the shell. Shells are used to interact with the operating system and execute commands.

    > **Example:**
    > ```  
    >{ ...
    >
    >   "shell": "/bin/bash"
    >    ...
    >}
    >```

    - **"home_dir"**: This key will create a home directory for the user. The value of this key will be a string that specifies the path where the home directory will be created, usually in the format of "/home/username". The home directory is the default working directory for the user when they log in to the system

    > **Example:**
    > ```  
    >{ ...
    >
    >   "home_dir": "/home/username"
    >    ...
    >}
    > ```
    >**IMPORTANT:** The home dir must be the same as the username, otherwise it could cause problems.

- **Example of an entire configuration file**

```
{
        "users": [ 
          {
            "username": "Zipi",
            "password": "1q2w3e4r5t6y",
            "shell": "/bin/bash",
            "home_dir": "/home/bob"
          },
          {
            "username": "Zape",
            "password": "1y2t3r4e5w6q",
            "shell": "/bin/bash",
            "home_dir": "/home/sponge"
          }
        ]
}
```
### **1.1 [OPTIONAL]** **Configuration File "B"**

To do the checks faster and easier, I created a counter script to delete users and the configuration file it's a **config.json** and only contains the **name of the users** to remove, you can see an example below:

```
[
    "Zipi",
    "Zape"
]
```

## **2. Create the script python**

To create the python script we will need the following modules:

```
import json
import os
import subprocess
import crypt
```

- **json**: We import this module to read de config.json file for the configurations.

- **os**:  We import this module to create some conditions to execute the script

- **subprocess**: We import this module to run the command to create the users.

-  **crypt**: We import this module to encrypt the password`s users to create

To run this script we will need be a privileges user `root`. So for achivement we will create the following condition on the script.

```
if os.geteuid() != 0:
    print("Error: This script must be run with root privileges.")
    exit()
```

### **Comprobation**

