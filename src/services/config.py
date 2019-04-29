import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('PG_CONNECTION_URI')
    AMQP_URI = os.getenv('AMQP_URI')
