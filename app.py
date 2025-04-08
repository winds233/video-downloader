import os
from flask import Flask, request, render_template, send_file
import yt_dlp
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    uid = str(uuid.uuid4())

    if format_type == 'mp3':
        output_path = os.path.join(DOWNLOAD_FOLDER, f'{uid}.mp3')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        output_path = os.path.join(DOWNLOAD_FOLDER, f'{uid}.mp4')
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    final_path = output_path if os.path.exists(output_path) else output_path.replace('.mp4', '.webm')
    return send_file(final_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
