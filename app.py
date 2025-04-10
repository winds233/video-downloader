

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
        filename = f'{uid}.mp3'
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'cookies.txt',
        }

    elif format_type == 'mp4':
        filename = f'{uid}.mp4'
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'cookiefile': 'cookies.txt',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return render_template('index.html', download_link=f'/download_file/{filename}')

@app.route('/download_file/<filename>')
def download_file(filename):
from flask import Flask, render_template, request, send_from_directory
import os
import uuid
import yt_dlp
import threading

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def baixar_video_em_thread(url, format_type, filename):
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path.replace('.mp3', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'cookies.txt',
        }

    elif format_type == 'mp4':
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'cookiefile': 'cookies.txt',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    uid = str(uuid.uuid4())

    filename = f'{uid}.{format_type}'

    # Inicia o download em segundo plano
    thread = threading.Thread(target=baixar_video_em_thread, args=(url, format_type, filename))
    thread.start()

    return render_template('index.html', download_link=f'/download_file/{filename}')

@app.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)



