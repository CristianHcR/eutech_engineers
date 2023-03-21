import os 
import subprocess
import json 
import crypt


with open('config.json') as f:
    e = json.load(f)

password = e['password']

print(password)
print(encrypted_password)