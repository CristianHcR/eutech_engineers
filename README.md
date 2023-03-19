<center>
# Task: Automate Server Backup Script
</center>
## Configuration File 

Firstly , we will need a configuration file in our case  will be called "config.json" in our case its important that will a json extention because we will use that module specific :

And that one will have contain :
 - The path of the directories that we want to copy:  
```
{
  ...
  "directories": [
    {
      "source": "C:/Users/cristian/Desktop/example1",
      "destination": "backup_example1"
    },
    {
      "source": "C:/Users/cristian/Desktop/example2",
      "destination": "backup_example2"
    }
  ]
}
```
- The path where we want to save our backups:
```
{
...
  "backup_path": "c:/Users/cristian/Desktop/backup",
...
} 
```
- The max backups we want to need:
```
{
...
"max_backups": 5,
...
} 
```
All my configuration of the config.json file:
``` 
{
  "backup_path": "c:/Users/cristian/Desktop/backup",
  "max_backups": 5,
  "directories": [
    {
      "source": "C:/Users/cristian/Desktop/example1",
      "destination": "backup_example1"
    },
    {
      "source": "C:/Users/cristian/Desktop/example2",
      "destination": "backup_example2"
    }
  ]
}
```

## Python File

The modules we will need  for the scripts will be the next ones: 

```
import shutil, os, logging, datetime, json
```
**Shutil module:** For realize the backups.
**Os module:** For edit, and configure file.
**Logging:** For generate error log file.
**Datetime :** For inclued the current timestamp.
**Json:**  For execute the configuration file .

For the script will be use a def create_backup(config_file) and will be divided in 6 parts:

The first part:

It`s for iniciate  the configuration file .json.
```
def create_backup(config_file):
    # Load configuration file
    with open(config_file) as f:
        config = json.load(f)
    ...
```
The second part:

It`s for create a backup with timestamp.
```
    # Create backup directory with timestamp
    backup_dir = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = os.path.join(config['backup_path'], backup_dir)
    os.makedirs(backup_path)
```
The third part:

It`s for create a backup for each directory.
```
 # Backup each directory
    for directory in config['directories']:
        source = directory['source']
        dest = os.path.join(backup_path, directory['destination'])

        try:
            shutil.copytree(source, dest)
            logging.info(f"Directory {source} backed up successfully to {dest}")
        except Exception as e:
            logging.error(f"Error backing up directory {source}: {str(e)}")
```
The fourth part:
It`s for delete old backups that we stablished.
``` 
   # Delete old backups if necessary
    backups = sorted(os.listdir(config['backup_path']))
    while len(backups) > config['max_backups']:
        oldest_backup = backups[0]
        shutil.rmtree(os.path.join(config['backup_path'], oldest_backup))
        logging.info(f"Deleted backup {oldest_backup}")
        backups = backups[1:]
``` 
Finally for schedule our script you can use two ways:

The first way it`s on the own script for this we will need two new modules.
```
import shutil, os, logging, datetime, json, schedule, time
```
And add the following lines on the bottom of the script in python.
``` 
if __name__ == '__main__':

    # Set up logging
    logging.basicConfig(filename='backup.log', level=logging.INFO) 
    #Schedules
schedule.every(1).seconds.do(create_backup, config_file='config.json')   
   
    while True:
        schedule.run_pending()
        time.sleep(1)

We will choose the option that best fits our needs.
Examples:
Lines	Explain
schedule.every(10).seconds.do(job)	This command schedules the "job" function to run every 10 seconds.
schedule.every(10).minutes.do(job)	This command schedules the "job" function to run every 10 minutes.
schedule.every().hour.do(job)	This command schedules the "job" function to run every hour.
schedule.every().day.at("10:30").do(job)	This command schedules the "job" function to run every day at 10:30 AM.
schedule.every(5).to(10).minutes.do(job)	This command schedules the "job" function to run every 5 to 10 minutes, i.e. the job will run randomly between 5 to 10 minutes.
schedule.every().monday.do(job)	 This command schedules the "job" function to run every Monday.
schedule.every().wednesday.at("13:15").do(job) 	This command schedules the "job" function to run every Wednesday at 1:15 PM.
schedule.every().minute.at(":17").do(job)	This command schedules the "job" function to run every minute at the 17th second, i.e. the job will run every minute but only on the 17th second of each minute.
```
Full  python code script:
```
import os
import shutil
import json
import datetime
import logging
def create_backup(config_file):

# Load configuration file

    with open(config_file) as f:
        config = json.load(f)

# Create backup directory with timestamp

    backup_dir = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_path = os.path.join(config['backup_path'], backup_dir)
os.makedirs(backup_path)

# Backup each directory

    for directory in config['directories']:
        source = directory['source']
        dest = os.path.join(backup_path, directory['destination'])
        try:
            shutil.copytree(source, dest)
            logging.info(f"Directory {source} backed up successfully to {dest}")
        except Exception as e:
            logging.error(f"Error backing up directory {source}: {str(e)}")
# Delete old backups if necessary
    backups = sorted(os.listdir(config['backup_path']))
    while len(backups) > config['max_backups']:
        oldest_backup = backups[0]
        shutil.rmtree(os.path.join(config['backup_path'], oldest_backup))
        logging.info(f"Deleted backup {oldest_backup}")
        backups = backups[1:]
if __name__ == '__main__':

    # Set up logging
    logging.basicConfig(filename='backup.log', level=logging.INFO) 
    #Schedules
schedule.every(1).seconds.do(create_backup, config_file='config.json')   
   
    while True:
        schedule.run_pending()
        time.sleep(1)
``` 
And The second way to do the schedule it´s with external software: 

In Linux, you can use  ‘crontab’ and for the the contab file add the following line :
```
53 12 * * * python /path/to/your/script.py
```
This is  an example to run the script every day at 12:53.

In Windows, you can use Task Scheduler to schedule the script to run automatically. Here are the general steps:

1. Open Task Scheduler from the Start menu.
2. Click "Create Task" in the Actions pane on the right.
3. Give the task a name and select the appropriate settings on the General, Triggers, Actions, and Settings tabs.
4. On the Actions tab, click "New" and select "Start a program" as the action.
5. In the "Program/script" field, enter the path to your Python executable (e.g., C:\Python38\python.exe).
6. In the "Add arguments" field, enter the path to your Python script (e.g., C:\path\to\your\script.py).
7. Click "OK" to save the action and "OK" again to save the task.
8. Your script will now run automatically according to the schedule specified in the Task Schedul
