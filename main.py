import os
import shutil
import json
import datetime
import logging
import schedule
import time

def create_backup(config_file): 
    # Load configuration file
    with open(config_file) as f:
        config = json.load(f)

    logging.info(" Starting backup job...")
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
            logging.info(f" Directory {source} backed up successfully to {dest}")
        except Exception as e:
            logging.error(f" Error backing up directory {source}: {str(e)}")

    # Delete old backups if necessary
    backups = sorted(os.listdir(config['backup_path']))
    while len(backups) > config['max_backups']:
        oldest_backup = backups[0]
        shutil.rmtree(os.path.join(config['backup_path'], oldest_backup))
        logging.info(f" Deleted backup {oldest_backup}")
        backups = backups[1:]
    logging.info(" Backup job complete.")
    logging.info("-------------------------")
    

if __name__ == '__main__':

    # Set up logging
    logging.basicConfig(filename='backup.log', level=logging.INFO) 

    #Schedules

    schedule.every(1).seconds.do(create_backup, config_file='config.json')   # if you want do backups every "x" seconds
    #schedule.every(10).minutes.do(create_backup, config_file='config.json')  # if you want do backups every "x" seconds
    #schedule.every().hour.do(job)                                           # If you want do backups every "x" hours
    #schedule.every().day.at("10:30").do(job)                                # In a determinate hour every day
    #schedule.every(5).to(10).minutes.do(job)
    #schedule.every().monday.do(job)
    #schedule.every().wednesday.at("13:15").do(job)
    #schedule.every().minute.at(":17").do(job)
   
    while True:
        schedule.run_pending()
        time.sleep(1)
    