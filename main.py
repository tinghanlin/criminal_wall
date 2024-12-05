#run: python3 main.py [user name]
#example: python3 main.py timmy
from gui_module import CriminalWall
import os
import sounddevice as sd
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys
import glob
import shutil

if __name__ == "__main__":
    #delete some files
    #TODO: implement a way to delete files
    # for file in glob.glob("new_*"): 
    #     os.remove(file)

    user_name = sys.argv[1]


    #delete an exisiting user folder
    if os.path.exists(user_name):
        shutil.rmtree(user_name)
       
    #create a new user folder
    os.makedirs(user_name)

    #start the GUI
    app = QApplication(sys.argv)
    window = CriminalWall(sys.argv)
    window.show()
    sys.exit(app.exec())

    

    
    

