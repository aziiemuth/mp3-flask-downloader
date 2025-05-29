from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from script_download import search_and_download_song

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

@app.route('/')
def index():
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/download_song', methods=['POST'])
def download_song():
    song_name = request.form.get('song_name')
    result = search_and_download_song(song_name, output_path=DOWNLOAD_FOLDER)
    return jsonify(result)

@app.route('/downloads/<filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
