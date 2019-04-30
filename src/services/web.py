from flask import Flask, jsonify, make_response, request
from werkzeug.exceptions import HTTPException
from schemas import photos_serializer
from models import Photo
from celery import Celery
import json
import os
import uuid

AMQP_URI = os.getenv('AMQP_URI')
celery = Celery(__name__, broker=AMQP_URI)
app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(success=True)


@app.route("/photos/pending")
def photos():
    all_photos = Photo.query.filter(Photo.status == 'pending')
    result = photos_serializer.dump(all_photos)
    return make_response(jsonify(result.data), 200)


@app.route("/photos/process", methods=['POST'])
def process_photos():
    data = json.loads(request.get_data())
    if isinstance(data, list):
        create_thumbnails(data)
    else:
        return make_response(
            jsonify(error='Expecting an array of photo uuids'),
            400)

    return make_response(jsonify(success=True), 201)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


def create_thumbnails(uuids):
    for uuid in uuids:
        if(is_valid_uuid(uuid)):
            celery.send_task('create_thumbnail', kwargs={'uuid': uuid}, queue='photo-processor')
            print(uuid)


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
