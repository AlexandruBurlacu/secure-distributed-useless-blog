import sqlalchemy as db

import os


__CONNECTION = None
__ENGINE = None


def get_blogs_table_handle():
    metadata = db.MetaData()
    blogs = db.Table("blogs", metadata, autoload=True, autoload_with=__ENGINE)
    return blogs


def get_db_connection():
    global __CONNECTION
    global __ENGINE
    if __CONNECTION:
        return __CONNECTION
    else:
        __ENGINE = db.create_engine(os.environ["DATABASE_URL"])
        __CONNECTION = __ENGINE.connect()
        return __CONNECTION
