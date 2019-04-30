from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import mapper
from database import metadata, db_session
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, DATE
from uuid import uuid4


class Photo(object):
    query = db_session.query_property()

    def __init__(self, uuid=None, url=None, status=None):
        self.uuid = uuid
        self.url = url
        self.status = status

    def __repr__(self):
        return '<Photo %r> [%r] %r' % (self.uuid, self.status, self.url)


class Thumbnail(object):
    query = db_session.query_property()

    def __init__(self, photo_uuid=None,
                 width=None, height=None, url=None):
        self.photo_uuid = photo_uuid
        self.width = width
        self.height = height
        self.url = url

photos = Table(
    'photos', metadata,
    Column('uuid', UUID(as_uuid=True), primary_key=True),
    Column('url', String),
    Column('status', String),
    Column('created_at', DateTime)
)

thumbnails = Table(
    'photo_thumbnails', metadata,
    Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('photo_uuid', UUID(as_uuid=True), ForeignKey('photos.uuid')), 
    Column('width', Integer),
    Column('height', Integer),
    Column('url', String),
    Column('created_at', DateTime, server_default=func.now())
)

mapper(Photo, photos)
mapper(Thumbnail, thumbnails)
