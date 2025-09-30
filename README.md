
<img width="737" height="520" alt="Screenshot 2025-09-30 at 7 01 39 AM" src="https://github.com/user-attachments/assets/6e5562c5-adbf-4450-b04b-d70ef4ca3d4c" />

````markdown
# SoundCloud Scraper App

A Python GUI tool that automates monitoring your SoundCloud stream, detects the currently playing track, and downloads it automatically at 320kbps MP3 using [yt-dlp](https://github.com/yt-dlp/yt-dlp).  

The app uses **PySide6** for the interface and **Selenium** with Chrome for playback monitoring.

---

## ✨ Features
- 🎵 Automatically detects the current SoundCloud track while you listen.  
- ⬇️ Downloads tracks in **320kbps MP3** format with clean filenames (`Artist - Title`).  
- 📜 Logs all activity in a scrollable console.  
- 📂 Stores downloaded files in a local `downloads/` folder.  
- ⏭️ Skip to next track with one click.  
- ▶️ Simple start/stop monitoring controls.  
- 💻 Cyberpunk-style GUI built with PySide6.

---

## 🚀 Requirements
- Python 3.9+  
- [Google Chrome](https://www.google.com/chrome/) installed  
- ChromeDriver (matching your Chrome version)  
- FFmpeg (for audio conversion)  

---

## 📦 Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/soundcloud-scraper-app.git
cd soundcloud-scraper-app
````

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` should include:

```
selenium
yt-dlp
PySide6
```

---

## ▶️ Usage

Run the app:

```bash
python app.py
```

1. Log in to your SoundCloud account inside the launched Chrome window.
2. Start playing your stream.
3. The app will automatically detect and download new tracks as you listen.

---

## 🖥️ GUI Controls

* **Start** → Launches monitoring of your SoundCloud stream.
* **Stop** → Ends monitoring and closes Chrome.
* **Next Track ▶** → Skips to the next track in the stream.

---

## 📁 Output

* All tracks are saved in the `downloads/` directory with the format:

```
Artist - Title.mp3
```

---

## ⚠️ Disclaimer

This tool is provided for **educational purposes only**.
Please respect copyright laws and the rights of creators when using this software.

---

