import tkinter as tk
from tkinter import messagebox, filedialog,ttk
import subprocess
import threading
import re
import sys
import os

def download_video():

    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    output_path = filedialog.askdirectory()
    if not output_path:
        messagebox.showinfo("Info", "Download cancelled.")
        return

   
    downloaded_video_label.config(text="")
    progress_label.config(text="")
    progress_bar["value"]=0
    root.update_idletasks()

    download_thread = threading.Thread(target=perform_download, args=(url, output_path))
    download_thread.start()

def perform_download(url, output_path):
    
    try:
        
        if sys.platform == "win32":
            
            yt_dlp_path = os.path.join(os.path.dirname(sys.executable), "Scripts", "yt-dlp.exe")
        else:
            
            yt_dlp_path = os.path.join(os.path.dirname(sys.executable), "yt-dlp")


        if not os.path.exists(yt_dlp_path):
            messagebox.showerror("Error", f"yt-dlp not found at: {yt_dlp_path}. Please check your installation.")
            return

        command = [
            yt_dlp_path, 
            "--force-generic-extractor",
            "-o", f"{output_path}/%(id)s.%(ext)s",
            url
        ]
        
       
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        
        filename = ""
        # Read output line by line
        for line in iter(process.stdout.readline, ""):
            if "Destination:" in line:
                filename = line.split("Destination: ")[-1].strip()
            
            # Use a regex to find the download percentage
            match = re.search(r'(\d+\.\d+)%', line)
            if match:
                progress = float(match.group(1))
                # Update the GUI on the main thread
                root.after(0, lambda p=progress: update_progress(p))
        
        process.stdout.close()
        process.wait()

        # Final UI update after download is complete
        root.after(0, lambda: finalize_download(filename))
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

def update_progress(progress):
    """Updates the progress bar and label."""
    progress_bar["value"] = progress
    progress_label.config(text=f"{progress:.2f}%")

def finalize_download(filename):
    """Updates the UI after the download is complete."""
    progress_bar["value"] = 100
    progress_label.config(text="100.00%")
    if filename:
        downloaded_video_label.config(text=f"Downloaded: {filename}", fg="black")
        messagebox.showinfo("Success", "Video downloaded successfully!")
    else:
        downloaded_video_label.config(text="Downloaded successfully, but filename not found.", fg="orange")



root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("450x200")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

url_label = tk.Label(main_frame, text="Enter YouTube URL:")
url_label.pack(pady=(0, 10))

url_entry = tk.Entry(main_frame, width=50)
url_entry.pack()

download_button = tk.Button(main_frame, text="Download Video", command=download_video)
download_button.pack(pady=(15, 0))

#progress bar widget
progress_bar = ttk.Progressbar(main_frame,orient="horizontal",length=300,mode="determinate")
progress_bar.pack(pady=(15,5))

progress_label = tk.Label(main_frame,text="")
progress_label.pack()

download_display_frame = tk.Frame(root, padx=20, pady=10)
download_display_frame.pack(fill="x")

downloaded_video_label = tk.Label(download_display_frame, text="", wraplength=400, justify="center")
downloaded_video_label.pack()

root.mainloop()
