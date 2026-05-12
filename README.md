# 🎥 YouTube Video Downloader

A simple desktop-based YouTube video downloader built using Python, Tkinter, and `yt-dlp`.

This application allows users to paste a YouTube URL, choose a download location, and download videos with a real-time progress bar.

---

## 📸 Preview

![App Preview](./assets/preview.png)

> Add a screenshot of your application inside an `assets` folder.

---

# ✨ Features

- 📥 Download YouTube videos
- 📊 Real-time download progress bar
- 🖥 Simple desktop GUI using Tkinter
- 📁 Choose custom download directory
- ⚡ Multithreaded downloading for smooth UI
- 🔔 Download completion notifications
- 🛠 Uses powerful `yt-dlp` backend

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Tkinter | GUI development |
| yt-dlp | Video downloading engine |
| threading | Background download processing |
| subprocess | Execute yt-dlp commands |
| ttk | Progress bar widget |

---

# 📂 Project Structure

```text
youtube-downloader/
│
├── main.py
├── README.md
├── requirements.txt
└── assets/
    └── preview.png
