from flask import Flask, request, send_file
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_audio():
    url = request.args.get('url')
    if not url:
        return "Error: No URL provided.", 400
    
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{yt.title}.mp3",
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run()
