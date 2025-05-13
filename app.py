from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube

app = Flask(__name__)
CORS(app)

@app.route('/getinfo')
def get_info():
    url = request.args.get('url')
    try:
        yt = YouTube(url)
        return jsonify({
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "streams": [
                {
                    "itag": s.itag,
                    "type": s.mime_type,
                    "res": s.resolution,
                    "abr": getattr(s, "abr", None),
                    "progressive": s.is_progressive
                } for s in yt.streams.filter(progressive=True).order_by('resolution').desc()
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/download')
def download():
    url = request.args.get('url')
    itag = request.args.get('itag')

    try:
        yt = YouTube(url)
        stream = yt.streams.get_by_itag(itag)
        download_url = stream.url  # This is a direct stream URL
        return jsonify({"download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
