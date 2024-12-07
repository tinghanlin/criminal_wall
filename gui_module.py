
# NOTE FROM CHARLOTTE - 
# the commented out version is the version that worked on timmys,
# underneath is my slightly adjusted one but wanted to keep both in here. 

# originally named "mainqt.py"
# Reference: https://realpython.com/python-pyqt-qthread/
# Reference: https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/

# required: PyQt6 & VLC
# in order to run - replace practice and test words with full list
# insert path to your VLC within the open_video function
# that should work! 
# notes: final video and message must be ONE mp4 file. (results.mp4)
# things to fix: update hanes gif for waiting page

# import sys
# import cv2
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
# from PyQt6.QtGui import QFont, QPixmap, QMovie
# from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
# import subprocess  
# from video_record_module import video_record
# import time
# import os


# #this is the background task for the GUI
# class SecretVideoRecord(QThread):

#     finished = pyqtSignal()

#     def __init__(self, video_filename, audio_filename, video_length, combine_filename, parent=None):
#         super().__init__(parent)
#         self.video_filename = video_filename
#         self.audio_filename = audio_filename
#         self.video_length = video_length
#         self.combine_filename = combine_filename

#     def run(self):
#         print("Starting secret video recording ... ")
#         video_record(self.video_filename, self.audio_filename, self.video_length, self.combine_filename)
#         self.finished.emit()
#         print("Secret video recording is completed! ")

# #this is the GUI
# class CriminalWall(QWidget):
#     def __init__(self, args):
#         super().__init__()
#         self.setWindowTitle("Criminal Wall")
#         self.user_name = args[1]
#         self.setFixedSize(600, 400)
#         #self.setFixedSize(int(3024/2), int(1964/2)) #Timmy I am just doing this to debug right now!
#         #self.setGeometry(100, 100, 600, 400)

#         # Fonts
#         self.title_font = QFont("Soleil", 60, QFont.Weight.Bold)
#         self.text_font = QFont("Soleil", 16)

#         # Main layout
#         self.main_layout = QVBoxLayout()
#         self.setLayout(self.main_layout)

#         # Background label for gif/static
#         self.bg_label = QLabel(self)
#         self.bg_label.setGeometry(0, 0, self.width(), self.height())
#         self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         self.dynamic_labels = []
#         self.current_bg = None
        
#         ###TODO: we might want to adjust these in the future###
#         self.video_length = 2 # in seconds
#         self.counter = 1
#         self.video_filename = self.user_name+"/new_video_"+str(self.counter)+".mp4"
#         self.audio_filename = self.user_name+"/new_audio_"+str(self.counter)+".wav"
#         self.combine_filename = self.user_name+"/new_combined_"+str(self.counter)+".mp4"
#         ###TODO: we might want to adjust these in the future###

#         # Unit data
#         self.practice_words = ["Bath", "Car", "Think"] #three specific words that can help detect accents
#         self.test_words = [ "A", "E", "I", "O", "U"]
#         # uncomment below for the actual test!
#         # self.test_words = [ "A",
#         #                     "E", 
#         #                     "I", 
#         #                     "O", 
#         #                     "U",
#         #                     "His",
#         #                     "Hers",
#         #                     "Its",
#         #                     "Is",
#         #                     "Was",
#         #                     "As",
#         #                     "Have",
#         #                     "Had",
#         #                     "For",
#         #                     "And",
#         #                     "If",
#         #                     "Not",
#         #                     "This",
#         #                     "That",
#         #                     "Join",
#         #                     "Unite",
#         #                     "Marry",
#         #                     "Your",
#         #                     "Fleece",
#         #                     "Feather",
#         #                     "Wind",
#         #                     "Rain",
#         #                     "Sun",
#         #                     "Snow",
#         #                     "What",
#         #                     "Why",
#         #                     "When",
#         #                     "Where",
#         #                     "Just",
#         #                     "Justice",
#         #                     "Silly",
#         #                     "Fun",
#         #                     "Little",
#         #                     "Tiny",
#         #                     "Beef",
#         #                     "Lamb",
#         #                     "Chicken",
#         #                     "White",
#         #                     "Black",
#         #                     "Letter",
#         #                     "Words",
#         #                     "File",
#         #                     "Data",
#         #                     "Accountability",
#         #                     "Responsibility"]

#         self.current_unit_index = 0

#         #self.showFullScreen() #Timmy added this to make it full screen when program is launched
#         self.show_welcome_page()

#     def resizeEvent(self, event):
#         """Handle window resize to ensure background scales."""
#         self.bg_label.setGeometry(0, 0, self.width(), self.height())
#         if isinstance(self.current_bg, QMovie):
#             self.current_bg.setScaledSize(self.size())
#         elif isinstance(self.current_bg, QPixmap):
#             self.bg_label.setPixmap(self.current_bg.scaled(
#                 self.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation
#             ))
#         super().resizeEvent(event)

#     def clear_layout(self):
#         """Clear layout while keeping background."""
#         # remove dynamically added (text labels, etc.)
#         for label in self.dynamic_labels:
#             label.deleteLater()  
#         self.dynamic_labels.clear()  # Clear the list of dynamic things

#         # other stuff like buttons
#         for i in reversed(range(self.main_layout.count())):
#             widget = self.main_layout.itemAt(i).widget()
#             if widget is not None:
#                 widget.deleteLater()  

#     # Pages
#     def show_welcome_page(self):
#         self.clear_layout()
#         self.set_background("1_landing_page.png") #page 1
#         self.add_transparent_button(self.show_instructions_page)

#     def show_instructions_page(self):
#         self.clear_layout()
#         self.set_background("2_instruction_page.png") #page 2
#         self.add_transparent_button(self.show_audio_instructions_page)

#     def show_audio_instructions_page(self):
#         self.clear_layout()
#         self.set_background("3_audio_reception.png") #page 3
#         self.add_transparent_button(self.show_practice_instructions_page)
    
#     def show_practice_instructions_page(self):
#         self.clear_layout()
#         self.set_background("4_pre_practice.png") #page 4
#         self.add_transparent_button(self.start_practice_units)

#     def start_practice_units(self):
#         """Start practice units with gif background."""
#         self.current_unit_index = 0
#         self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units, is_practice_round=True)

#     def finish_practice_units(self):
#         """Finish practice units and show transition page."""
#         self.clear_layout()
#         self.set_background("5_im_ready.png") #page 5
#         self.add_transparent_button(self.start_test_units)

#     def start_test_units(self):
#         """Start test units with gif background."""
#         self.current_unit_index = 0
#         self.show_unit_page_with_gif(self.test_words, self.show_wait_page, is_practice_round=False)

#     def show_unit_page_with_gif(self, words, completion_callback, is_practice_round=True):
#         """Show a single gif page with specific indicators for practice or test rounds."""
#         self.clear_layout()  # Clear any previous widgets to avoid overlapping content
#         self.set_background("bgfullv3.gif")

#         # showing "Practice Round __" ONLY for practice rounds
#         if is_practice_round:
            
#             practice_round = self.current_unit_index + 1  

#             #practice round label
#             round_label = QLabel(f"Practice Round {practice_round}", self)
#             round_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))  
#             round_label.setStyleSheet("color: blue;")  
#             round_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # Aligning
#             round_label.setGeometry(100, 100, 600, 300)  # positioning
#             round_label.show()

#             # addto dynamic_labels list so it clear later
#             self.dynamic_labels.append(round_label)

#         # "Speak the word..." ONLY for test rounds
#         if not is_practice_round:
#             speak_text = (
#                 '<p style="font-family:Soleil; font-size: 60px; color: grey; font-weight: bold;">'
#                 '<span style="color: blue;">speak</span> the <span style="color: grey;">word</span> that you see out loud.'                '</p>'
#             )
#             speak_label = QLabel(speak_text, self)
#             speak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             speak_label.setGeometry(0, self.height() // 5, self.width(), 100)  
#             speak_label.setWordWrap(True)  # wrapping if  text is too long
#             speak_label.show()

#             # dynamic_labels list for clearing
#             self.dynamic_labels.append(speak_label)

#         # show the current word 
#         if self.current_unit_index < len(words):
#             word = words[self.current_unit_index]
#         else:
#             completion_callback()
#             return

#         word_label = QLabel(self)
#         word_label.setText(word)
#         word_label.setFont(QFont("Soleil", 90, QFont.Weight.Bold))
#         word_label.setStyleSheet("""
#             color: darkgray;
#             background-color: rgba(0, 0, 0, 0);
#         """)
#         word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         word_label.setGeometry(0, self.height() // 2 - 50, self.width(), 100)
#         word_label.show()

#         # dynamic label clearning
#         self.dynamic_labels.append(word_label)

#         # timer to move to the next word/ finish gif
#         self.start_timer(6, lambda: self.show_next_word(words, completion_callback, is_practice_round))

#         #call video record
#         self.start_secret_video_record(self.video_filename, self.audio_filename, self.video_length, self.combine_filename)

       
#     def show_next_word(self, words, completion_callback, is_practice_round):
#         """Show the next word in the list."""
#         self.current_unit_index += 1
        
#         if self.current_unit_index < len(words):
#             self.show_unit_page_with_gif(words, completion_callback, is_practice_round)
#         else:
#             # end of current round of units
#             completion_callback()

#     def show_wait_page(self):
#         """Display the wait page before playing the videos."""
#         self.clear_layout()
#         self.set_background("background_wait.gif")
#         self.add_transparent_button(self.show_result_video) #TODO: something is wrong after this part


# # NON FULL SCREEN 
#     def show_result_video(self):
#         """Play  result video in external program"""
#         self.open_video("result.mp4")

#     def show_final_panel_page(self):
#         """Play final panel video in external program."""
#         self.open_video("panel.mp4")

# # no text on screen
#     def open_video(self, video_path):
#         """Open video in VLC media player in fullscreen without showing the title and pause at the last frame."""
#         try:
#             vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"  # Path to VLC binary
#             # Open VLC in fullscreen, pause at the last frame, and disable the title display
#             subprocess.Popen([vlc_path, "--fullscreen", "--play-and-pause", "--no-video-title-show", video_path])
#         except FileNotFoundError:
#             print("Error: VLC media player is not installed or path is incorrect.")
#         except Exception as e:
#             print(f"Error opening video {video_path} with VLC: {e}")

#     def set_background(self, path):
#         """Set background."""
#         # clear first
#         if isinstance(self.current_bg, QMovie):
#             self.current_bg.stop()
#             self.bg_label.clear()
#             self.current_bg = None

#         if path.endswith(".gif"):
#             movie = QMovie(path)
#             movie.setScaledSize(self.size())
#             self.bg_label.setMovie(movie)
#             movie.start()
#             self.current_bg = movie
#         else:
#             pixmap = QPixmap(path)
#             if pixmap.isNull():
#                 print(f"Error: Image {path} not found.")
#                 return
#             pixmap = pixmap.scaled(
#                 self.size(),
#                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
#                 Qt.TransformationMode.SmoothTransformation
#             )
#             self.bg_label.setPixmap(pixmap)
#             self.current_bg = pixmap

#     def add_transparent_button(self, callback):
#         """Add transparent button across the bottom half of the page"""
#         button = QPushButton("")
#         button.setStyleSheet("""
#             QPushButton {
#                 background-color: rgba(0, 0, 0, 0);
#                 border: none;
#             }
#         """)
#         button.setFixedHeight(self.height() // 2)
#         button.setFixedWidth(self.width())
#         button.clicked.connect(callback)
#         self.main_layout.addStretch()
#         self.main_layout.addWidget(button)

#     def start_timer(self, seconds, next_page_callback):
#         """Start a timer for transitions."""
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(next_page_callback)
#         self.timer.setSingleShot(True)
#         self.timer.start(seconds * 1000)
#         print("gif is done playing!")
    
#     #start a QThread for video recording
#     def start_secret_video_record(self, video_filename, audio_filename, video_length, combine_filename):
#         self.video_record_task = SecretVideoRecord(video_filename, audio_filename, video_length, combine_filename)
#         self.video_record_task.finished.connect(self.update_next_video_name)
#         self.video_record_task.start()

#     def update_next_video_name(self):
#         #update next video name
#         self.counter +=1
#         self.video_filename = self.user_name+"/new_video_"+str(self.counter)+".mp4"
#         self.audio_filename = self.user_name+"/new_audio_"+str(self.counter)+".wav"
#         self.combine_filename = self.user_name+"/new_combined_"+str(self.counter)+".mp4"
        

# ADJUSTED SCRIPT BY CHARLOTTE FOR HER COMPUTER & FULL SCREEN

import sys
import cv2
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
import subprocess
from video_record_module import video_record
import time
import os


# Background task for the GUI
class SecretVideoRecord(QThread):
    finished = pyqtSignal()

    def __init__(self, video_filename, audio_filename, video_length, combine_filename, parent=None):
        super().__init__(parent)
        self.video_filename = video_filename
        self.audio_filename = audio_filename
        self.video_length = video_length
        self.combine_filename = combine_filename

    def run(self):
        try:
            print("Starting secret video recording...")
            video_record(self.video_filename, self.audio_filename, self.video_length, self.combine_filename)
            print(f"Recorded video: {self.video_filename}, audio: {self.audio_filename}")
            
            # FFmpeg command to combine video and audio
            command = [
                "ffmpeg", "-y", "-i", self.video_filename, "-i", self.audio_filename,
                "-c:v", "libx264", "-c:a", "aac", "-shortest", self.combine_filename
            ]
            subprocess.run(command, check=True)
            print("Combined video and audio successfully.")
            self.finished.emit()
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
        except Exception as e:
            print(f"Unexpected error during recording: {e}")


# The GUI
class CriminalWall(QWidget):
    def __init__(self, args):
        super().__init__()
        self.setWindowTitle("Criminal Wall")
        self.user_name = args[1]

        # Fonts
        self.title_font = QFont("Soleil", 60, QFont.Weight.Bold)
        self.text_font = QFont("Soleil", 16)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Background label
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.dynamic_labels = []
        self.current_bg = None

        # Variables for recording
        self.video_length = 2
        self.counter = 1
        self.video_filename = f"{self.user_name}/new_video_{self.counter}.mp4"
        self.audio_filename = f"{self.user_name}/new_audio_{self.counter}.wav"
        self.combine_filename = f"{self.user_name}/new_combined_{self.counter}.mp4"

        # Words for practice and testing
        self.practice_words = ["Bath", "Car", "Think"]
        self.test_words = ["A", "B", "C"]
        self.current_unit_index = 0

        # Open in full screen
        self.showFullScreen()
        self.setFixedSize(self.width(), self.height())

        self.show_welcome_page()

    def resizeEvent(self, event):
        """Handle window resize to ensure background scales."""
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        
        if isinstance(self.current_bg, QMovie):
            self.current_bg.setScaledSize(self.size())
        elif isinstance(self.current_bg, QPixmap):
            self.bg_label.setPixmap(self.current_bg.scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,  # Fill the screen
                Qt.TransformationMode.SmoothTransformation
            ))
        print(f"Window size: {self.size()}, bg_label size: {self.bg_label.size()}")
        super().resizeEvent(event)

    def clear_layout(self):
        """Clear layout while keeping background."""
        for label in self.dynamic_labels:
            label.deleteLater()
        self.dynamic_labels.clear()

        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    # Pages
    def show_welcome_page(self):
        self.clear_layout()
        self.set_background("1_landing_page.png")
        self.add_transparent_button(self.show_instructions_page)

    def show_instructions_page(self):
        self.clear_layout()
        self.set_background("2_instruction_page.png")
        self.add_transparent_button(self.show_audio_instructions_page)

    def show_audio_instructions_page(self):
        self.clear_layout()
        self.set_background("3_audio_reception.png")
        self.add_transparent_button(self.show_practice_instructions_page)
    
    def show_practice_instructions_page(self):
        self.clear_layout()
        self.set_background("4_pre_practice.png")
        self.add_transparent_button(self.start_practice_units)

    def start_practice_units(self):
        """Start practice units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units, is_practice_round=True)

    def finish_practice_units(self):
        """Finish practice units and show transition page."""
        self.clear_layout()
        self.set_background("5_im_ready.png")
        self.add_transparent_button(self.start_test_units)

    def start_test_units(self):
        """Start test units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.test_words, self.show_wait_page, is_practice_round=False)

    def show_unit_page_with_gif(self, words, completion_callback, is_practice_round=True):
        """Show a single gif page with specific indicators for practice or test rounds."""
        self.clear_layout()
        self.set_background("bgfullv3.gif")

        if is_practice_round:
            practice_round = self.current_unit_index + 1
            round_label = QLabel(f"Practice Round {practice_round}", self)
            round_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))
            round_label.setStyleSheet("color: blue;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            round_label.setGeometry(100, 100, 600, 300)
            round_label.show()
            self.dynamic_labels.append(round_label)

        if not is_practice_round:
            speak_text = (
                '<p style="font-family:Soleil; font-size: 60px; color: grey; font-weight: bold;">'
                '<span style="color: blue;">speak</span> the <span style="color: grey;">word</span> that you see out loud.'
                '</p>'
            )
            speak_label = QLabel(speak_text, self)
            speak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            speak_label.setGeometry(0, self.height() // 5, self.width(), 100)
            speak_label.setWordWrap(True)
            speak_label.show()
            self.dynamic_labels.append(speak_label)

        if self.current_unit_index < len(words):
            word = words[self.current_unit_index]
        else:
            completion_callback()
            return

        word_label = QLabel(self)
        word_label.setText(word)
        word_label.setFont(QFont("Soleil", 90, QFont.Weight.Bold))
        word_label.setStyleSheet("color: darkgray; background-color: rgba(0, 0, 0, 0);")
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_label.setGeometry(0, self.height() // 2 - 50, self.width(), 100)
        word_label.show()
        self.dynamic_labels.append(word_label)

        self.start_timer(6, lambda: self.show_next_word(words, completion_callback, is_practice_round))
        self.start_secret_video_record(self.video_filename, self.audio_filename, self.video_length, self.combine_filename)

    def show_next_word(self, words, completion_callback, is_practice_round):
        self.current_unit_index += 1
        if self.current_unit_index < len(words):
            self.show_unit_page_with_gif(words, completion_callback, is_practice_round)
        else:
            completion_callback()

    def show_wait_page(self):
        self.clear_layout()
        self.set_background("background_wait.gif")
        self.add_transparent_button(self.show_result_video)

    def show_result_video(self):
        self.open_video("result.mp4")

    def show_final_panel_page(self):
        self.open_video("panel.mp4")

    def open_video(self, video_path):
        try:
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
            subprocess.Popen([vlc_path, "--fullscreen", "--play-and-pause", "--no-video-title-show", video_path])
        except FileNotFoundError:
            print("Error: VLC media player is not installed or path is incorrect.")
        except Exception as e:
            print(f"Error opening video {video_path} with VLC: {e}")

    def set_background(self, path):
        if isinstance(self.current_bg, QMovie):
            self.current_bg.stop()
            self.bg_label.clear()
            self.current_bg = None

        if path.endswith(".gif"):
            movie = QMovie(path)
            movie.setScaledSize(self.size())
            self.bg_label.setMovie(movie)
            movie.start()
            self.current_bg = movie
        else:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                print(f"Error: Image {path} not found.")
                return
            pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,  # Fill the screen
                Qt.TransformationMode.SmoothTransformation
            )
            self.bg_label.setPixmap(pixmap)
            self.current_bg = pixmap

    def add_transparent_button(self, callback):
        button = QPushButton("")
        button.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 0); border: none; }")
        button.setFixedHeight(self.height() // 2)
        button.setFixedWidth(self.width())
        button.clicked.connect(callback)
        self.main_layout.addStretch()
        self.main_layout.addWidget(button)

    def start_timer(self, seconds, next_page_callback):
        self.timer = QTimer(self)
        self.timer.timeout.connect(next_page_callback)
        self.timer.setSingleShot(True)
        self.timer.start(seconds * 1000)
        print("gif is done playing!")

    def start_secret_video_record(self, video_filename, audio_filename, video_length, combine_filename):
        self.video_record_task = SecretVideoRecord(video_filename, audio_filename, video_length, combine_filename)
        self.video_record_task.finished.connect(self.update_next_video_name)
        self.video_record_task.start()

    def update_next_video_name(self):
        self.counter += 1
        self.video_filename = f"{self.user_name}/new_video_{self.counter}.mp4"
        self.audio_filename = f"{self.user_name}/new_audio_{self.counter}.wav"
        self.combine_filename = f"{self.user_name}/new_combined_{self.counter}.mp4"
