import sys
import threading
import cv2
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from pydub import AudioSegment
from pydub.playback import play


class DissonanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dissonance")
        self.setGeometry(100, 100, 800, 600)
        self.show_result_video()

    def play_audio(self, audio_path):
        """Play audio using pydub."""
        try:
            audio = AudioSegment.from_file(audio_path)
            play(audio)
        except FileNotFoundError:
            print(f"Audio file not found: {audio_path}")

    def play_video(self, video_path, audio_path, callback):
        """Play video with audio."""
        cap = cv2.VideoCapture(video_path)

        # Set OpenCV window to fullscreen
        cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Play audio in a separate thread
        audio_thread = threading.Thread(target=self.play_audio, args=(audio_path,))
        audio_thread.start()

        # Read and display video frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        callback()

    def show_result_video(self):
        self.play_video("result.mp4", "result_audio.mp3", self.show_final_panel_page)

    def show_final_panel_page(self):
        self.play_video("panel.mp4", "panel_audio.mp3", lambda: print("Final video finished."))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DissonanceApp()
    window.show()
    sys.exit(app.exec())
