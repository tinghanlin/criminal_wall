

# required: PyQt6 & opencv-python & VLC

import sys
import cv2
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer
import subprocess  


class DissonanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dissonance")
        self.setGeometry(100, 100, 600, 400)

        # Fonts
        self.title_font = QFont("Soleil", 60, QFont.Weight.Bold)
        self.text_font = QFont("Soleil", 16)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Background label for gif/static
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dynamic_labels = []
        self.current_bg = None

        # Unit data
        self.practice_words = ["practice1", "practice2", "practice3"]
        self.test_words = [f"test{i}" for i in range(1, 4)]
        self.current_unit_index = 0

       
        self.show_welcome_page()

    def resizeEvent(self, event):
        """Handle window resize to ensure background scales."""
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        if isinstance(self.current_bg, QMovie):
            self.current_bg.setScaledSize(self.size())
        elif isinstance(self.current_bg, QPixmap):
            self.bg_label.setPixmap(self.current_bg.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            ))
        super().resizeEvent(event)

    def clear_layout(self):
        """Clear layout while keeping background."""
        # remove dynamically added (text labels, etc.)
        for label in self.dynamic_labels:
            label.deleteLater()  
        self.dynamic_labels.clear()  # Clear the list of dynamic things

        # other stuff like buttons
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  

    # Pages
    def show_welcome_page(self):
        self.clear_layout()
        self.set_background("background_welcome_new.png")
        self.add_transparent_button(self.show_instructions_page)

    def show_instructions_page(self):
        self.clear_layout()
        self.set_background("background_instructions_new.png")
        self.add_transparent_button(self.show_audio_instructions_page)

    def show_audio_instructions_page(self):
        self.clear_layout()
        self.set_background("background_audio_new.png")
        self.add_transparent_button(self.start_practice_units)

    def start_practice_units(self):
        """Start practice units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units, is_practice_round=True)

    def finish_practice_units(self):
        """Finish practice units and show transition page."""
        self.clear_layout()
        self.set_background("background_ready.png")
        self.add_transparent_button(self.start_test_units)

    def start_test_units(self):
        """Start test units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.test_words, self.show_wait_page, is_practice_round=False)

    def show_unit_page_with_gif(self, words, completion_callback, is_practice_round=True):
        """Show a single gif page with specific indicators for practice or test rounds."""
        self.clear_layout()  # Clear any previous widgets to avoid overlapping content
        self.set_background("bgfullnew.gif")

        # showing "Practice Round __" ONLY for practice rounds
        if is_practice_round:
            
            practice_round = self.current_unit_index + 1  

            #practice round label
            round_label = QLabel(f"practice round {practice_round}", self)
            round_label.setFont(QFont("Soleil", 40, QFont.Weight.Bold))  
            round_label.setStyleSheet("color: blue;")  
            round_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  # Aligning
            round_label.setGeometry(100, 100, 600, 300)  # positioning
            round_label.show()

            # addto dynamic_labels list so it clear later
            self.dynamic_labels.append(round_label)

        # "Speak the word..." ONLY for test rounds
        if not is_practice_round:
            speak_text = (
                '<p style="font-family:Soleil; font-size: 60px; color: grey; font-weight: bold;">'
                '<span style="color: blue;">speak</span> the <span style="color: grey;">word</span> that you see out loud.'                '</p>'
            )
            speak_label = QLabel(speak_text, self)
            speak_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            speak_label.setGeometry(0, self.height() // 5, self.width(), 100)  
            speak_label.setWordWrap(True)  # wrapping if  text is too long
            speak_label.show()

            # dynamic_labels list for clearing
            self.dynamic_labels.append(speak_label)

        # show the current word 
        if self.current_unit_index < len(words):
            word = words[self.current_unit_index]
        else:
            completion_callback()
            return

        word_label = QLabel(self)
        word_label.setText(word)
        word_label.setFont(QFont("Soleil", 90, QFont.Weight.Bold))
        word_label.setStyleSheet("""
            color: darkgray;
            background-color: rgba(0, 0, 0, 0);
        """)
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_label.setGeometry(0, self.height() // 2 - 50, self.width(), 100)
        word_label.show()

        # dynamic label clearning
        self.dynamic_labels.append(word_label)

        # timer to move to the next word/ finish gif
        self.start_timer(4, lambda: self.show_next_word(words, completion_callback, is_practice_round))

    def show_next_word(self, words, completion_callback, is_practice_round):
        """Show the next word in the list."""
        self.current_unit_index += 1
        
        if self.current_unit_index < len(words):
            self.show_unit_page_with_gif(words, completion_callback, is_practice_round)
        else:
            # end of current round of units
            completion_callback()

    def show_wait_page(self):
        """Display the wait page before playing the videos."""
        self.clear_layout()
        self.set_background("background_wait_new.png")
        self.add_transparent_button(self.show_result_video)


# NON FULL SCREEN 
    def show_result_video(self):
        """Play  result video in external program"""
        self.open_video("result.mp4")

    def show_final_panel_page(self):
        """Play final panel video in external program."""
        self.open_video("panel.mp4")

    # def open_video(self, video_path):
    #     """Open video in the default system """
    #     try:
    #         subprocess.Popen(["open", video_path])  # macOS: "open", Windows: "start", Linux: "xdg-open"
    #     except Exception as e:
    #         print(f"Error opening video {video_path}: {e}")
    #     finally:
    #         #  close the app after the video is opened?
    #         self.close()
    






    #VERISION WITH QUICKTIME PLAYER FULL SCREEN

    # def show_result_video(self):
    #     """Play result video in external program."""
    #     self.open_video_in_fullscreen("result.mp4")

    # def show_final_panel_page(self):
    #     """Play final panel video in external program."""
    #     self.open_video_in_fullscreen("panel.mp4")

# version not working with fullscreen
    # def open_video_in_fullscreen(self, video_path):
    #     """Open the video in QuickTime Player."""
    #     import subprocess
    #     try:
    #         subprocess.run(["open", video_path], check=True)
    #     except FileNotFoundError:
    #         print("Error: QuickTime Player could not open the file.")





    # VERSION with FULL SCREEN  VLC

# version with text on screen
    def open_video(self, video_path):
        """Open video in VLC media player in fullscreen and pause at the last frame."""
        try:
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC" #replace path wherever we r playing from
            # Open VLC in fullscreen mode and pause at the last frame
            subprocess.Popen([vlc_path, "--fullscreen", "--play-and-pause", video_path])
        except FileNotFoundError:
            print("Error: VLC media player is not installed or path is incorrect.")
        except Exception as e:
            print(f"Error opening video {video_path} with VLC: {e}")

    def open_video(self, video_path):
        """Open video in VLC media player in fullscreen without showing the title and pause at the last frame."""
        try:
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"  # Path to VLC binary
            # Open VLC in fullscreen, pause at the last frame, and disable the title display
            subprocess.Popen([vlc_path, "--fullscreen", "--play-and-pause", "--no-video-title-show", video_path])
        except FileNotFoundError:
            print("Error: VLC media player is not installed or path is incorrect.")
        except Exception as e:
            print(f"Error opening video {video_path} with VLC: {e}")





    def show_final_page(self):
        """Display the final page and keep it until the program is exited"""
        self.clear_layout()
        self.set_background("finalpg.png")

    def set_background(self, path):
        """Set background."""
        # clear first
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
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.bg_label.setPixmap(pixmap)
            self.current_bg = pixmap

    def add_transparent_button(self, callback):
        """Add transparent button across the bottom half of the page"""
        button = QPushButton("")
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
            }
        """)
        button.setFixedHeight(self.height() // 2)
        button.setFixedWidth(self.width())
        button.clicked.connect(callback)
        self.main_layout.addStretch()
        self.main_layout.addWidget(button)

    def start_timer(self, seconds, next_page_callback):
        """Start a timer for transitions."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(next_page_callback)
        self.timer.setSingleShot(True)
        self.timer.start(seconds * 1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DissonanceApp()
    window.show()
    sys.exit(app.exec())


