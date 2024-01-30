import os
import shutil
import time
import argparse
from datetime import datetime

def sync_folders(source_folder, backup_folder, log_file):
    try:
        if os.path.exists(backup_folder)!= True:
            os.makedirs(backup_folder)

        for root, dirs, files in os.walk(source_folder):
            for file in files:
                source_path = os.path.join(root, file)
                backup_path = os.path.join(backup_folder, os.path.relpath(source_path, source_folder))

                if os.path.exists(backup_path) != True or os.path.getmtime(source_path) > os.path.getmtime(backup_path):
                    shutil.copy2(source_path, backup_path)
                    log_operation("COPY", source_path, backup_path, log_file)

        for root, dirs, files in os.walk(backup_folder):
            for file in files:
                backup_path = os.path.join(root, file)
                source_path = os.path.join(source_folder, os.path.relpath(backup_path, backup_folder))

                if os.path.exists(source_path) != True:
                    os.remove(backup_path)
                    log_operation("REMOVE", source_path, backup_path, log_file)

    except Exception as e:
        log_operation("ERROR", str(e), "", log_file)

def log_operation(action, source_path, backup_path, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} {action}: {source_path} -> {backup_path}\n"
    
    print(log_entry, end="\n")

    with open(log_file, "a") as log:
        log.write(log_entry)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_folder")
    parser.add_argument("backup_folder")
    parser.add_argument("interval", type=int)
    parser.add_argument("log_file")
    args = parser.parse_args()

    print("Folder synchronization started. Press Ctrl+C to stop.")
    open(args.log_file, 'w').close()

    try:
        while True:
            sync_folders(args.source_folder, args.backup_folder, args.log_file)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nFolder synchronization stopped.")

if __name__ == "__main__":
    main()
