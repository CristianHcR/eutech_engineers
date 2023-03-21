import subprocess
import json
import os

# Check if script is being run with root privileges
if os.geteuid() != 0:
    print("Error: This script must be run with root privileges.")
    exit()

# Read the configuration file
with open('config.json', 'r') as f:
    usernames = json.load(f)

# Delete the user accounts
for username in usernames:
    cmd = f"userdel {username} \
           --remove \
           --force"

    subprocess.run(cmd.split(), check=True)

    # Check if the user was deleted
    try:
        subprocess.run(f"id {username}".split(), check=True)
        print(f"Error: Failed to delete user {username}.")
    except subprocess.CalledProcessError:
        print(f"User {username} was deleted successfully!")
