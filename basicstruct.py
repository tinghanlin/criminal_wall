

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer


class DissonanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dissonance")
        self.setGeometry(100, 100, 600, 400)

        # fonts
        self.title_font = QFont("Times New Roman", 18, QFont.Weight.Bold)
        self.text_font = QFont("Times New Roman", 14)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Background labels for GIF / static
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.current_bg = None  

        # words for units
        self.practice_words = ["practice1", "practice2", "practice3"]
        self.test_words = [f"test{i}" for i in range(1, 4)]
        self.current_unit_index = 0

        self.show_welcome_page()

    def resizeEvent(self, event):
        """ window resize to make sure the background scales."""
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
        while self.main_layout.count():
            widget = self.main_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()
        self.bg_label.clear()

    # Pages
    def show_welcome_page(self):
        self.clear_layout()
        self.set_background("background_welcome.png")
        self.add_transparent_button(self.show_instructions_page)

    def show_instructions_page(self):
        self.clear_layout()
        self.set_background("background_instructions.png")
        self.add_transparent_button(self.show_audio_instructions_page)

    def show_audio_instructions_page(self):
        self.clear_layout()
        self.set_background("background_audio.png")
        self.add_transparent_button(self.start_practice_units)

    def start_practice_units(self):
        """Start practice units with the GIF background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units)

    def finish_practice_units(self):
        """Finish practice units and show transition page."""
        self.clear_layout()
        self.set_background("background_ready.png")
        self.add_transparent_button(self.start_test_units)

    def start_test_units(self):
        """Start test units with GIF background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.test_words, self.show_end_sequence)

    def show_unit_page_with_gif(self, words, completion_callback):
        """Show GIF page for practice / test units."""
        self.clear_layout()

        
        self.set_background("bgfull.gif")

        # Schedule transition
        self.start_timer(3, lambda: self.show_next_word(words, completion_callback))

    def show_next_word(self, words, completion_callback):
        """Show the next word in the list."""
        self.current_unit_index += 1
        if self.current_unit_index < len(words):
            self.show_unit_page_with_gif(words, completion_callback)
        else:
            completion_callback()

    def show_end_sequence(self):
        """Show the waiting page."""
        self.clear_layout()
        self.set_background("background_wait.png")
        self.add_transparent_button(self.show_video_page)

    def show_video_page(self):
        """Show the video background page."""
        self.clear_layout()
        self.set_background("background_vid.png")
        self.add_transparent_button(self.show_final_panel_page)

    def show_final_panel_page(self):
        """Show the final panel page."""
        self.clear_layout()
        self.set_background("background_panel.png")
        end_label = QLabel("Thank you for participating!", self)
        end_label.setFont(self.title_font)
        end_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(end_label)

    # helpers
    def set_background(self, path):
        """Set the background, supporting both static images and GIFs."""
        if path.endswith(".gif"):
            # Gif background
            movie = QMovie(path)
            movie.setScaledSize(self.size())  
            self.bg_label.setMovie(movie)
            movie.start()
            self.current_bg = movie  
        else:
            # static image background
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
        """transparent button on bottom half of the page."""
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
        """Start timer for page transitions."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(next_page_callback)
        self.timer.setSingleShot(True)
        self.timer.start(seconds * 1000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DissonanceApp()
    window.show()
    sys.exit(app.exec())
