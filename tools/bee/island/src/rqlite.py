import uuid
import utils
import logging
import pystache

from contextlib import contextmanager
import pyrqlite.dbapi2 as dbapi2

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

RQLITE_SERVER = utils.env('RQLITE_SERVER', 'localhost')
RQLITE_PORT = utils.env('RQLITE_PORT', 4001, int)


def get_connection(conn=None):

    if conn is not None:
        return conn

    # Connect to the database
    _conn = dbapi2.connect(host=RQLITE_SERVER, port=RQLITE_PORT,)
    logger.debug("connection opened")
    return _conn

@contextmanager
def get_closable_connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        logger.debug("closing connection...")
        conn.close()

def get_cursor(conn=None):
    _conn = get_connection(conn) if conn is None else conn
    return _conn.cursor()

def execute(command, params=(), conn=None):
    with get_cursor(conn) as cursor:
        cursor.execute(command, params)

def execute_many(command, params, conn=None):
    with get_cursor(conn) as cursor:
        cursor.executemany(command, seq_of_parameters=params)

def fetch_fields(cursor, one=False, fields=[]):
    if one:
        rs = cursor.fetchone()
        if rs is None or len(rs) == 0:
            return None

        logger.debug("rs => %s %s", str(rs), str(fields))
        return {f: rs[f] for f in fields}

    rss = cursor.fetchmany()
    logger.debug("rs => %s %s", str(rss), str(fields))
    if rss is None or len(rss) == 0:
        return []

    return [{f: rs[f] for f in fields} for rs in rss]

def fetch(cursor, one=False, parser=None, fields=[]):
    if parser is None and len(fields) == 0:
        return cursor.fetchone() if one else cursor.fetchmany()[0:]

    if parser is not None:
        return parser(cursor.fetchone()) if one else parser(cursor.fetchmany())

    return fetch_fields(cursor, one, fields)

def find_one(query, params=(), parser=None, fields=[], conn=None):
    with get_cursor(conn) as cursor:
        cursor.execute(query, params)
        return fetch(cursor, True, parser, fields)

def find(query, params=(), parser=None, fields=[], conn=None):
    with get_cursor(conn) as cursor:
        cursor.execute(query, params)
        return fetch(cursor, False, parser, fields)
