from flask import Flask, render_template, request, jsonify, send_file, Response
import yt_dlp
import os
import requests
from urllib.parse import urlparse
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    url = request.json.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title')
            uploader = info.get('uploader')
            thumbnail = info.get('thumbnail')
            video_url = info.get('url')

            return jsonify({
                'title': title,
                'uploader': uploader,
                'thumbnail': thumbnail,
                'video_url': video_url
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download')
def download():
    video_url = request.args.get('video_url')
    filename = request.args.get('filename', 'video.mp4')

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(video_url, stream=True, headers=headers)
    file_stream = BytesIO(response.content)

    return send_file(file_stream, as_attachment=True, download_name=filename, mimetype='video/mp4')

@app.route('/thumbnail_proxy')
def thumbnail_proxy():
    url = request.args.get('url')
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        return Response(response.content, content_type=response.headers['Content-Type'])
    except Exception as e:
        return f"Error loading image: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
