# Reference: https://realpython.com/python-pyqt-qthread/
# Reference: https://www.pythonguis.com/tutorials/pyqt6-creating-your-first-window/
import sys
import cv2
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
import subprocess
from video_record_module import video_record
import time
import os
from video_edit_personal_module import triple_video_edit
from video_edit_group_module import video_edit_full
import random

# background recording task for the GUI
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

# background video-editting task for the GUI
class SecretVideoEdit(QThread):
    finished = pyqtSignal()
    
    def __init__(self, user_name, debug_flag, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.debug_flag = debug_flag

    def run(self):
        #edit sing, psa1, psa2 video for the current user
        triple_video_edit(self.user_name, self.debug_flag) 
        #create group psa videos and combine the final video
        video_edit_full(self.user_name, self.debug_flag)
        self.finished.emit()

# The GUI
class CriminalWall(QWidget):
    def __init__(self, user_name, debug_flag, parent=None):
        super().__init__()
        self.setWindowTitle("Criminal Wall")
        self.user_name = user_name
        self.debug_flag = debug_flag

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
        ###TODO: we might want to adjust these in the future###
        self.video_length = 2 #two seconds
        ###TODO: we might want to adjust these in the future###
        self.counter = 1
        self.video_filename = f"{self.user_name}/new_video_{self.counter}.mp4"
        self.audio_filename = f"{self.user_name}/new_audio_{self.counter}.wav"
        self.combine_filename = f"{self.user_name}/new_combined_{self.counter}.mp4"

        ###TODO: we might want to adjust these in the future###
        self.wait_time_for_video_generation = 40
        ###TODO: we might want to adjust these in the future###

        # Words for practice and testing
        self.practice_words = ["Bath", "Car", "Think"]

        if debug_flag == True:
            #if you want to change this, make sure to also change the corresponding dictionary in video_edit_personal_module.py
            self.test_words = ["A", "E", "I"]
        else:
            self.test_words = [
                "A",
                "E",
                "I",
                "O",
                "U",
                "His",
                "Hers",
                "Its",
                "Is",
                "Was",
                "As",
                "Have",
                "Had",
                "For",
                "And",
                "If",
                "Not",
                "This",
                "That",
                "Join",
                "Unite",
                "Marry",
                "Your",
                "Fleece",
                "Feather",
                "Wind",
                "Rain",
                "Sun",
                "Snow",
                "What",
                "Why",
                "When",
                "Where",
                "Just",
                "Justice",
                "Silly",
                "Fun",
                "Little",
                "Tiny",
                "Beef",
                "Lamb",
                "Chicken",
                "White",
                "Black",
                "Letter",
                "Words",
                "File",
                "Data",
                "Accountability",
                "Responsibility"]
        self.test_words_length = len(self.test_words)
        self.current_unit_index = 0

        # Open in full screen
        self.showFullScreen()
        self.setFixedSize(self.width(), self.height())

        self.show_welcome_page()

        #list of pre-coded accents
        self.list_of_accents = [
            "General Northern (New York, Michigan)",
            "New England (Boston, Maine)",
            "Western New England (Vermont, New Hampshire)",
            "General Midwestern (Ohio, Wisconsin, Michigan)",
            "Chicago/Chicagoan",
            "North-Central (Minnesota, Wisconsin)",
            "General Southern (Texas, Georgia, Alabama, Carolinas)",
            "Coastal Southern (Louisiana, Mississippi)",
            "Texan",
            "California (Southern California, Northern California)",
            "Pacific Northwest (Washington, Oregon)",
            "Southwestern (Arizona, New Mexico)",
            "Appalachian English (Kentucky, West Virginia, Tennessee)",
            "Mid-Atlantic (Philadelphia, Baltimore)"
        ]

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
        self.set_background("assets/1_landing_page.png")
        self.add_transparent_button(self.show_instructions_page)

    def show_instructions_page(self):
        self.clear_layout()
        self.set_background("assets/2_instruction_page.png")
        self.add_transparent_button(self.show_audio_instructions_page)

    def show_audio_instructions_page(self):
        self.clear_layout()
        self.set_background("assets/3_audio_reception.png")
        self.add_transparent_button(self.show_practice_instructions_page)
    
    def show_practice_instructions_page(self):
        self.clear_layout()
        self.set_background("assets/4_pre_practice.png")
        self.add_transparent_button(self.start_practice_units)

    def start_practice_units(self):
        """Start practice units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units, is_practice_round=True)

    def finish_practice_units(self):
        """Finish practice units and show transition page."""
        self.clear_layout()
        self.set_background("assets/5_im_ready.png")
        self.add_transparent_button(self.start_test_units)

    def start_test_units(self):
        """Start test units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.test_words, self.show_wait_page, is_practice_round=False)

    def show_unit_page_with_gif(self, words, completion_callback, is_practice_round=True):
        """Show a single gif page with specific indicators for practice or test rounds."""
        self.clear_layout()
        self.set_background("assets/bgfullv3.gif")

        if is_practice_round:
            practice_round = self.current_unit_index + 1
            round_label = QLabel(f"Practice Round {practice_round}/3", self)
            round_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))
            round_label.setStyleSheet("color: blue;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            round_label.setGeometry(100, 100, 600, 300)
            round_label.show()
            self.dynamic_labels.append(round_label)

        if not is_practice_round:
            test_round = self.current_unit_index + 1
            round_label = QLabel(f"Test Round {test_round}/"+str(self.test_words_length), self)
            round_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))
            round_label.setStyleSheet("color: blue;")
            round_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            round_label.setGeometry(100, 100, 600, 300)
            round_label.show()
            self.dynamic_labels.append(round_label)

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

        #each word is 6 seconds of waiting, allowing background video recording to complete
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
        self.set_background("assets/background_wait.gif")
        
        # we are waiting here to generate the final video!
        self.start_timer(self.wait_time_for_video_generation, self.show_wait_done_page)
        self.start_secret_triple_video_edit(self.user_name, self.debug_flag)
    

    def show_wait_done_page(self):
        self.clear_layout()
        self.set_background("assets/6_done.png")
        self.add_transparent_button(self.show_result_video)

    def show_result_video(self):
        self.open_video("final.mp4")
        self.add_transparent_button(self.show_accent_prediction)

    def show_accent_prediction(self):
        self.clear_layout()
        self.set_background("assets/7_end.png")
        random_accent_index = random.randint(1, len(self.list_of_accents))-1
        accent_label = QLabel(f"Thank you for participating!<br>We predict your accent is:<br>{self.list_of_accents[random_accent_index]}", self)
        accent_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))
        accent_label.setStyleSheet("color: black;")
        accent_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        accent_label.setGeometry(100, 400, 1200, 300)
        accent_label.show()
        self.dynamic_labels.append(accent_label)

    def open_video(self, video_path):
        try:
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
            subprocess.Popen([vlc_path, "--fullscreen", "--play-and-pause", "--no-video-title-show", video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #Note: When exiting the VLC, we need to go back to close the pyqt window.

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

    def start_secret_triple_video_edit(self, user_name, debug_flag):
        self.triple_video_edit_task = SecretVideoEdit(user_name, debug_flag)
        self.triple_video_edit_task.start()

    def update_next_video_name(self):
        self.counter += 1
        self.video_filename = f"{self.user_name}/new_video_{self.counter}.mp4"
        self.audio_filename = f"{self.user_name}/new_audio_{self.counter}.wav"
        self.combine_filename = f"{self.user_name}/new_combined_{self.counter}.mp4"
