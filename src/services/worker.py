import sys
import os
import time
import logging
from celery import Celery
from database import db_session
from models import Photo, Thumbnail
from urllib.request import urlopen
from PIL import Image, ImageOps
from pathlib import Path

AMQP_URI = os.getenv('AMQP_URI')
celery = Celery(__name__, broker=AMQP_URI)


@celery.task(name='create_thumbnail')
def create_thumbnail(uuid):

    photo = Photo.query.filter(Photo.uuid == uuid).one()

    try:
        logging.info(
            'processing photo {} '.format(photo.uuid))

        # resize and add transparent background
        size = (320, 320)
        im = Image.open(urlopen(photo.url))
        im.thumbnail(size, Image.ANTIALIAS)
        background = Image.new('RGBA', size, (255, 255, 255, 0))
        background.paste(im,
                         (int((size[0] - im.size[0]) / 2),
                          int((size[1] - im.size[1]) / 2)))
        relative_filename = Path(uuid).with_suffix('.png')
        filename = Path('/waldo-app-thumbs', uuid).with_suffix('.png')
        background.save(filename, "png")

        # todo: save in the location from the environment
        thumbnail = Thumbnail(photo.uuid, 320, 320, str(relative_filename))

        db_session.add(thumbnail)
        photo.status = 'completed'
        db_session.add(photo)
        db_session.commit()

    except Exception as e:
        logging.error('generation error {} {}'.format(uuid, str(e)))
        photo.status = 'failed'
        db_session.add(photo)
        db_session.commit()
