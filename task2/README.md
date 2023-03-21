# **Automate User Account Creation Script**

## **Objective**
The objective for this task it's create a script on python to create multiple users on linux this script will must contain the username, password user, home directory and shell.

## **Materials**
For do this task we will need:

- Python installed, in this case **"python 3.10"** 
-  S.O Linux, in this case **"ubuntu 20.04"**

## **Development**

## **1. Create the configuration json file**

First of all, we will create a .json file in this case "config.json":

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
    >**IMPORTANT:** The house name must be the same as the username otherwise it could cause problems.

    


## **2. Create the script python**

### **Comprobation**

