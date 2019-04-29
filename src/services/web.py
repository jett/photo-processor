from flask import Flask, jsonify
from schemas import photos_serializer
from models import Photo

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(success=True)


@app.route("/photos/pending")
def photos():
    all_photos = Photo.query.filter(Photo.status == 'pending')
    result = photos_serializer.dump(all_photos)
    return jsonify(result.data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
