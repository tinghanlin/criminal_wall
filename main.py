#run: python3 main.py [user name] [--debug]
#example: python3 main.py timmy 
# Reference: https://docs.python.org/3/library/argparse.html
from gui_module import CriminalWall
import os
import sounddevice as sd
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys
import glob
import shutil
import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    #use argparse to handle command line inputs
    parser = argparse.ArgumentParser(description = "Ask Timmy how to run the code!")
    parser.add_argument('user_name', type=str, help="A user name is required to create a database for that user")
    parser.add_argument('--debug', action='store_true', help="If this optional flag is included, we will turn on the debug mode.")
    args = parser.parse_args()

    if args.debug:
        print("Debug mode")
        debug_flag = True
    else:
        print("Full experience mode")
        debug_flag = False

    user_name = args.user_name

    #delete an exisiting user folder
    if os.path.exists(user_name): 
        shutil.rmtree(user_name) 
    
    #create a new user folder
    os.makedirs(user_name)

    #make sure necessary folders are all created
    folders = [
        "debug",
        "debug_psa1",
        "debug_psa1_adjusted",
        "debug_psa2",
        "debug_psa2_adjusted",
        "full_experience",
        "full_experience_psa1",
        "full_experience_psa1_adjusted",
        "full_experience_psa2",
        "full_experience_psa2_adjusted"
    ]

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created {folder} folder")

    #start the GUI
    try:
        app = QApplication(sys.argv)
        window = CriminalWall(user_name, debug_flag)
        window.show()
        sys.exit(app.exec())

    except Exception as e:
        logging.error(f"Error occurred: {e}")
    
    

