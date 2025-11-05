from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>YouTube Downloader</h1>
    <form action="/download" method="post">
        <input type="text" name="url" placeholder="Enter YouTube Video URL" required>
        <select name="format">
            <option value="mp3">MP3</option>
            <option value="mp4">MP4</option>
        </select>
        <button type="submit">Download</button>
    </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_choice = request.form['format']
    output_template = '%(title)s.%(ext)s'
    
    # Use yt-dlp to download the media
    ydl_opts = {
        'format': 'bestaudio' if format_choice == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio' if format_choice == 'mp3' else 'FFmpegVideoConvertor',
            'preferredformat': 'mp3' if format_choice == 'mp3' else 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Create the file path and serve it
    file_name = output_template.replace('%(title)s', ydl.prepare_filename(ydl.extract_info(url, download=False)))
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
