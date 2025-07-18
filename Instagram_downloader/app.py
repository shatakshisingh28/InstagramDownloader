from flask import Flask, render_template, request, redirect, url_for, flash
import os
import yt_dlp

app = Flask(__name__)
app.secret_key = "secret123"

DOWNLOAD_DIR = os.path.join("static", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("Please enter a URL.", "danger")
            return redirect(url_for("index"))

        try:
            ydl_opts = {
                "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            flash("Video downloaded successfully!", "success")
        except Exception as e:
            flash(f"Error: {e}", "danger")

        return redirect(url_for("index"))

    # List files (latest first)
    files = os.listdir(DOWNLOAD_DIR)
    files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(DOWNLOAD_DIR, f)), reverse=True)

    return render_template("index.html", files=files)

if __name__ == "__main__":
    app.run(debug=True)
