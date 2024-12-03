


import sys
import cv2
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QMovie
from PyQt6.QtCore import Qt, QTimer


class DissonanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dissonance")
        self.setGeometry(100, 100, 600, 400)

        # Fonts
        self.title_font = QFont("Soleil", 24, QFont.Weight.Bold)
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

        # Start the application
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
        while self.main_layout.count():
            widget = self.main_layout.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

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
        """Start practice units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.practice_words, self.finish_practice_units)

    def finish_practice_units(self):
        """Finish practice units and show transition page."""
        self.clear_layout()
        self.set_background("background_ready.png")
        self.add_transparent_button(self.start_test_units)

    def start_test_units(self):
        """Start test units with gif background."""
        self.current_unit_index = 0
        self.show_unit_page_with_gif(self.test_words, self.show_wait_page)

    def show_unit_page_with_gif(self, words, completion_callback):
        """Show a single gif page."""
        self.clear_layout()
        self.set_background("bgfullnew.gif")

        if self.current_unit_index < len(words):
            word = words[self.current_unit_index]
        else:
            completion_callback()
            return

        word_label = QLabel(self)
        word_label.setText(word)
        word_label.setFont(QFont("Soleil", 36, QFont.Weight.Bold))
        word_label.setStyleSheet("""
            color: darkgray;  /* Text color */
            background-color: rgba(0, 0, 0, 0);  /* Fully transparent background */
        """)
        word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_label.setGeometry(0, self.height() // 2 - 50, self.width(), 100)
        word_label.show()
        self.main_layout.addWidget(word_label)

        self.start_timer(3, lambda: self.show_next_word(words, completion_callback))

    def show_next_word(self, words, completion_callback):
        """Show the next word in the list."""
        self.current_unit_index += 1
        self.show_unit_page_with_gif(words, completion_callback)

    def show_wait_page(self):
        """Display the wait page before playing the videos."""
        self.clear_layout()
        self.set_background("background_wait.png")
        self.add_transparent_button(self.show_result_video)

    def play_video(self, video_path, callback):
        """Play video using OpenCV and clear layout"""
        self.clear_layout()
        self.current_bg = None 
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video file {video_path}")
            callback()
            return

        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit on 'q' 
                break

        cap.release()
        cv2.destroyAllWindows()
        callback()

    def show_result_video(self):
        """Play the result video and transition to the final panel video."""
        self.play_video("result.mp4", self.show_final_panel_page)

    def show_final_panel_page(self):
        """Play the final panel video and transition to the final page."""
        self.play_video("panel.mp4", self.show_final_page)

    def show_final_page(self):
        """Display the final page and keep it until the program is exited."""
        self.clear_layout()
        self.set_background("finalpg.png")

    # Helpers
    def set_background(self, path):
        """Set background."""
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
        """Add transparent button across the bottom half of the page."""
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
