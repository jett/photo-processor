from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import mapper
from database import metadata, db_session


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

    def __init__(self, uuid=None, photo_uuid=None,
                 width=None, height=None, url=None, created_at=None):
        self.uuid = uuid
        self.photo_uuid = photo_uuid
        self.width = width
        self.height = height
        self.url = url
        self.created_at = created_at

photos = Table(
    'photos', metadata,
    Column('uuid', String, primary_key=True),
    Column('url', String),
    Column('status', String),
    Column('created_at', DateTime)
)

thumbnails = Table(
    'photo_thumbnail', metadata,
    Column('uuid', String, primary_key=True),
    Column('photo_uuid', ForeignKey('photos.uuid')),
    Column('width', Integer),
    Column('height', Integer),
    Column('url', String),
    Column('created_at', DateTime)
)

mapper(Photo, photos)
mapper(Thumbnail, thumbnails)


# if __name__ == '__main__':
#     from sqlalchemy.orm import scoped_session, sessionmaker, Query
#     items = Photo.query.all()
#     print(len(items))
