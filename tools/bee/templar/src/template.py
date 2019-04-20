import uuid
import utils
import logging
import pystache
from pybars import Compiler

import pyrqlite.dbapi2 as dbapi2

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

compiler = Compiler()
compiled_templates = {}

RQLITE_SERVER = utils.env('RQLITE_SERVER', 'localhost')
RQLITE_PORT = utils.env('RQLITE_PORT', 4001, int)

# Connect to the database
connection = dbapi2.connect(host=RQLITE_SERVER, port=RQLITE_PORT,)

with connection.cursor() as cursor:
    cursor.execute('CREATE TABLE IF NOT EXISTS template (id text not null primary key, value text)')

def get(id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT value FROM template WHERE id = ?', (id,))
        result = cursor.fetchone()
        return None if result is None else result['value']

def update(id, _template):
    logger.info("Updating template '%s' => {%s}..." % (id, _template))
    with connection.cursor() as cursor:
        cursor.execute('UPDATE template SET value = ? WHERE id = ?', (_template, id,))
    global compiled_templates
    compiled_templates = {}

def save(id, _template):
    _t = get(id)
    logging.info("%s => %s" % (id, _t))
    if _t:
        update(id, _template)
    else:
        logger.info("Saving template '%s' => {%s}..." % (id, _template))
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO template(id, value) VALUES(?, ?)', (id, _template,))

def delete(id):
    logger.info("Deleting template '%s'..." % (id))
    with connection.cursor() as cursor:
        cursor.execute('DELETE template WHERE id = ?', (id,))
    global compiled_templates
    compiled_templates = {}

def compile_v1(id, binds):
    logger.info("[v1]template [%s] => [%s]", id, str(binds))
    _template = get(id)
    if _template:
        return pystache.render(_template, binds)
    return None

def get_compiled_template(id):
    if id in compiled_templates:
        logger.info("Template '%s' already compiled", id)
        return compiled_templates[id]

    _t = get(id)
    if _t:
        _ct = compiler.compile(_t)
        compiled_templates[id] = _ct
        return _ct
    return None

def _templar_helper(this, options, id, binds):
    logger.info("template helper [%s] => [%s]", id, str(binds))
    _template = get_compiled_template(id)
    if _template:
        return _template(binds, helpers={'templar': _templar_helper})
    return [u'']

def compile_v2(id, binds):
    logger.info("[v2]template [%s] => [%s]", id, str(binds))
    _template = get_compiled_template(id)
    if _template:
        return _template(binds, helpers={'templar': _templar_helper})
    return None
