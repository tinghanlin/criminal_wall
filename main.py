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

if __name__ == "__main__":
    #use argparse to handle command line inputs
    parser = argparse.ArgumentParser(description = "Ask Timmy how to run the code!")
    parser.add_argument('user_name', type=str, help="A user name is required to create a database for that user")
    parser.add_argument('--debug', action='store_true', help="If this optional flag is included, we will turn on the debug mode.")
    args = parser.parse_args()

    if args.debug:
        print("Debug mode is turned on")
        debug_flag = True
    else:
        print("No debug mode")
        debug_flag = False

    user_name = args.user_name

    ##TODO: this block is commented out to debug, so please remove once finish debuging
    #delete an exisiting user folder
    if os.path.exists(user_name): 
        shutil.rmtree(user_name) 
       
    #create a new user folder
    os.makedirs(user_name)
    ##TODO: this block is commented out to debug

    if not os.path.exists("debug"):
        os.makedirs("debug")
        print("Create debug folder")
        
    if not os.path.exists("full_experience"):
        os.makedirs("full_experience")
        print("Create full_experience folder")
        
    #start the GUI
    app = QApplication(sys.argv)
    window = CriminalWall(user_name, debug_flag)
    window.show()
    sys.exit(app.exec())

    

    
    

