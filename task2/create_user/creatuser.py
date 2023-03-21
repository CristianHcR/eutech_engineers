import os
import json
import subprocess
import crypt

if os.geteuid() != 0:
    print("Error: This script must be run with root privileges.")
    exit()


# Read the JSON configuration file
with open('config.json') as f:
    users_data = json.load(f)

# Create users
for user in users_data['users']:
  # Extract the username from configuration file 
    username = user['username']
  # Extract the password from configuration file   
    password = user['password']
  # Encrypt the password  
    salt = "saltstring"
    encrypted_password = crypt.crypt(password, salt)
  # Extract the shell from configuration file   
    shell = user['shell']
  # Extract the home_dir from configuration file   
    home_dir = user['home_dir']
  # Run the `useradd` command to create the user with specified shell and home directory
    subprocess.run(['useradd', '-m', '-p', encrypted_password, '-s', shell, '-d', home_dir, username])
    print(f"Created user '{username}' with password '{password}', shell '{shell}', and home directory '{home_dir}'")