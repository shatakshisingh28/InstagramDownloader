import os
import tkinter as tk
from tkinter import messagebox
from downloader import download_video

# Setup download folder
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    try:
        download_video(url, DOWNLOAD_DIR)
        messagebox.showinfo("Success", f"Downloaded to: {DOWNLOAD_DIR}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("Instagram Downloader")
root.geometry("400x200")
root.configure(bg="white")

tk.Label(root, text="Instagram Video Downloader", font=("Arial", 14), bg="white").pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

tk.Button(root, text="Download", bg="#1da1f2", fg="white", command=start_download).pack(pady=10)

root.mainloop()
