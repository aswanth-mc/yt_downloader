import tkinter as tk

root = tk.Tk()
root.title("youtube downloader")
root.geometry("400x150")

main_frame = tk.Frame(root,padx=20,pady=20)
main_frame.pack(fill="both",expand=True)

url_label = tk.Label(main_frame,text="enter the url")
url_label.pack(pady=(0,10))

url_entry = tk.Entry(main_frame,width=50)
url_entry.pack()

download_button = tk.Button(main_frame,text="download video")
download_button.pack()

root.mainloop()