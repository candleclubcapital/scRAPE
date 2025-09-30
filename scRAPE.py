import sys
import os
import time
import re
import yt_dlp

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import QThread, Signal


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


class TrackMonitor(QThread):
    track_found = Signal(str)
    log_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.driver = None
        self.visited_tracks = set()
        self.running = True

    def setup_driver(self):
        self.log_message.emit("Launching Chrome...")

        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        profile_path = os.path.expanduser("~/sc-chrome-profile")

        options = Options()
        options.binary_location = chrome_path
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service=ChromeService(), options=options)
        self.log_message.emit("Chrome launched.")

    def sanitize_filename(self, text):
        return re.sub(r'[\\/*?:"<>|]', '', text)

    def get_current_track(self):
        try:
            elem = self.driver.find_element(By.CLASS_NAME, "playbackSoundBadge__titleLink")
            href = elem.get_attribute("href")
            return href
        except:
            return None

    def download_track(self, url):
        try:
            info = yt_dlp.YoutubeDL({'quiet': True}).extract_info(url, download=False)
            title = info.get("title", "UnknownTitle")
            artist = info.get("uploader", "UnknownArtist")
            filename = self.sanitize_filename(f"{artist} - {title}")

            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/{filename}.%(ext)s',
                'format': 'bestaudio/best',
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log_message.emit(f"Downloaded: {filename}.mp3")
        except Exception as e:
            self.log_message.emit(f"Download failed: {e}")

    def skip_to_next_track(self):
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.SHIFT, Keys.RIGHT)
            self.log_message.emit("Skipped to next track.")
        except Exception as e:
            self.log_message.emit(f"Failed to skip: {e}")

    def run(self):
        try:
            self.setup_driver()
            self.driver.get("https://soundcloud.com/stream")
            self.log_message.emit("Log into SoundCloud and press Play.")

            while self.running:
                url = self.get_current_track()
                if url and url not in self.visited_tracks:
                    self.visited_tracks.add(url)
                    self.track_found.emit(url)
                    self.download_track(url)
                time.sleep(10)
        except Exception as e:
            self.log_message.emit(f"Critical error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                self.log_message.emit("Chrome closed.")

    def stop(self):
        self.running = False


class SoundCloudScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoundCloud Rapist")
        self.setGeometry(100, 100, 750, 500)
        self.setStyleSheet("background-color: #111; color: #0f0; font-family: monospace; font-size: 14px;")

        self.layout = QVBoxLayout()

        self.status_label = QLabel("Status: Ready")
        self.layout.addWidget(self.status_label)

        self.track_list = QListWidget()
        self.layout.addWidget(self.track_list)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        button_row = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_monitoring)
        button_row.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        button_row.addWidget(self.stop_button)

        self.skip_button = QPushButton("Next Track ▶")
        self.skip_button.clicked.connect(self.skip_track)
        self.skip_button.setEnabled(False)
        button_row.addWidget(self.skip_button)

        self.layout.addLayout(button_row)
        self.setLayout(self.layout)
        self.monitor_thread = None

    def add_track(self, url):
        self.track_list.addItem(url)

    def update_log(self, message):
        self.status_label.setText(f"Status: {message}")
        self.log_output.append(message)

    def start_monitoring(self):
        self.monitor_thread = TrackMonitor()
        self.monitor_thread.track_found.connect(self.add_track)
        self.monitor_thread.log_message.connect(self.update_log)
        self.monitor_thread.start()
        self.update_log("Monitoring started.")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.skip_button.setEnabled(True)

    def stop_monitoring(self):
        if self.monitor_thread:
            self.monitor_thread.stop()
            self.monitor_thread.quit()
            self.monitor_thread.wait()
            self.update_log("Monitoring stopped.")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.skip_button.setEnabled(False)

    def skip_track(self):
        if self.monitor_thread and self.monitor_thread.driver:
            self.monitor_thread.skip_to_next_track()


def main():
    app = QApplication(sys.argv)
    window = SoundCloudScraperApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
