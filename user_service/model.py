import sqlalchemy as db

import os


__CONNECTION = None
__ENGINE = None

def get_users_table_handle():
    metadata = db.MetaData()
    users = db.Table("users", metadata, autoload=True, autoload_with=__ENGINE)
    return users


def get_db_connection():
    global __CONNECTION
    global __ENGINE
    if __CONNECTION:
        return __CONNECTION
    else:
        __ENGINE = db.create_engine(os.environ["DATABASE_URL"])
        __CONNECTION = __ENGINE.connect()
        return __CONNECTION
