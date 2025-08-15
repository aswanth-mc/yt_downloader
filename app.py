import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import threading
import re
import sys
import os

def download_video():
    """
    Downloads a YouTube video using yt-dlp.
    """
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    output_path = filedialog.askdirectory()
    if not output_path:
        messagebox.showinfo("Info", "Download cancelled.")
        return

    # Clear the previous download message
    downloaded_video_label.config(text="")
    root.update_idletasks() # Force UI update

    # Use threading to prevent the GUI from freezing during the download
    download_thread = threading.Thread(target=perform_download, args=(url, output_path))
    download_thread.start()

def perform_download(url, output_path):
    """
    Performs the actual download using the yt-dlp command.
    This function runs in a separate thread.
    """
    try:
        # Determine the correct path to the yt-dlp executable
        # This will work whether the script is run in a virtual environment or not
        if sys.platform == "win32":
            # On Windows, executables are typically in the 'Scripts' directory
            yt_dlp_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "yt-dlp.exe")
        else:
            # On Linux/macOS, they are typically in the 'bin' directory
            yt_dlp_path = os.path.join(os.path.dirname(sys.executable), "yt-dlp")

        # Check if the executable exists
        if not os.path.exists(yt_dlp_path):
            messagebox.showerror("Error", f"yt-dlp not found at: {yt_dlp_path}. Please check your installation.")
            return

        command = [
            yt_dlp_path,  # Use the full path here
            "--force-generic-extractor",
            "-o", f"{output_path}/%(id)s.%(ext)s",
            url
        ]
        
        # Run the command and capture the output
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Parse the output to find the downloaded filename
        filename = ""
        for line in result.stdout.splitlines():
            # Look for the line that says "Destination:"
            if "Destination:" in line:
                filename = line.split("Destination: ")[-1]
                break
        
        # After the download is complete, update the UI
        if filename:
            downloaded_video_label.config(text=f"Downloaded: {filename}", fg="black")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        else:
            downloaded_video_label.config(text="Downloaded successfully, but filename not found.", fg="orange")

    except FileNotFoundError:
        # This catch is now less likely to happen with the path check, but good to have.
        messagebox.showerror("Error", "yt-dlp not found. Please install it with 'pip install yt-dlp'.")
        
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred during download:\n{e.stderr}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

# --- GUI Setup ---

root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("450x200") # Adjusted window size

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

url_label = tk.Label(main_frame, text="Enter YouTube URL:")
url_label.pack(pady=(0, 10))

url_entry = tk.Entry(main_frame, width=50)
url_entry.pack()

download_button = tk.Button(main_frame, text="Download Video", command=download_video)
download_button.pack(pady=(15, 0))

# A new frame to display the downloaded video info
download_display_frame = tk.Frame(root, padx=20, pady=10)
download_display_frame.pack(fill="x")

downloaded_video_label = tk.Label(download_display_frame, text="", wraplength=400, justify="center")
downloaded_video_label.pack()

root.mainloop()
