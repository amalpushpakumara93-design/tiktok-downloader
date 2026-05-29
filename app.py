from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_tiktok(url):
    ydl_opts = {
        'outtmpl': 'tiktok_video.mp4',
        'format': 'best',
        'quiet': True
    }
    try:
        if os.path.exists('tiktok_video.mp4'):
            os.remove('tiktok_video.mp4')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return 'tiktok_video.mp4'
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "ලින්ක් එකක් ඇතුළත් කර නැත.", 400

    file_path = download_tiktok(url)

    if file_path and os.path.exists(file_path):
        response = send_file(file_path, as_attachment=True)
        @response.call_on_close
        def remove_file():
            if os.path.exists(file_path):
                os.remove(file_path)
        return response
    else:
        return "වීඩියෝව බාගත කිරීමට නොහැකි විය.", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
