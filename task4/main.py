import os
import datetime
import shutil
import time
def check_directories(directories, log_file):
    all_directories_checked = True
    for directory in directories:
        try:
            os.listdir(directory)
            print(f"{directory} is accessible.")
        except OSError as e:
            all_directories_checked = False
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            error_message = f"{timestamp} - Error checking directory {directory}: {str(e)}"
            print(f"{directory} is not accessible.")
            with open(log_file, "a") as file:
                file.write(f"ERROR: {error_message}\n")
    return all_directories_checked

def backup_directories(source_directories, destination_directory, log_file):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}"
    backup_directory = os.path.join(destination_directory, backup_filename)
    os.makedirs(backup_directory)
    
    all_directories_copied = True
    for source_directory in source_directories:
        destination_subdirectory = os.path.join(backup_directory, os.path.basename(source_directory))
        try:
            shutil.copytree(source_directory, destination_subdirectory)
            print(f"{source_directory} copied successfully.")
        except Exception as e:
            all_directories_copied = False
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            error_message = f"{timestamp} - Error copying directory {source_directory}: {str(e)}"
            print(f"{source_directory} could not be copied.")
            print(error_message)
            with open(log_file, "a") as file:
                file.write(f"ERROR: {error_message}\n")
    
    if all_directories_copied:
        
        print(f"Backup completed successfully.")
    else:
        print("Backup could not be completed successfully. See log file for details.")

source_directories = ["example1", "example2"]
destination_directory = "backup"
log_file = "error.log"

all_directories_checked = False
attempt_count = 0
max_attempts = 3
while not all_directories_checked and attempt_count < max_attempts:
    all_directories_checked = check_directories(source_directories, log_file)
    attempt_count += 1
    if not all_directories_checked:
        print(f"Directories check failed. Retrying in 1 minute ({attempt_count}/{max_attempts})...")
        time.sleep(2)

if all_directories_checked:
    backup_directories(source_directories, destination_directory, log_file)
