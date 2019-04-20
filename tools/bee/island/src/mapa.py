import uuid
import json
import rqlite
import logging

import utils
import templar
import rabbitmq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

exchange = utils.env('EXCHANGE', 'octopus')
queue_name = utils.env('QUEUE', 'island_file_gen')
routing_key = utils.env('INPUT_RK', 'file_generate')

rabbit_conn = rabbitmq.get_connection()
rabbitmq.create_exchange(exchange, rabbit_conn);
rabbitmq.create_queue(queue_name, exchange, routing_key, rabbit_conn)

with rqlite.get_closable_connection() as conn:
    logger.info("Loading database tables....")
    # map
    rqlite.execute('''CREATE TABLE IF NOT EXISTS map (
                            id text not null primary key,
                            name text not null,
                            description text)''', conn=conn)
    # file_map - with map and templar reference
    rqlite.execute('''CREATE TABLE IF NOT EXISTS file_map (
                            id text not null primary key,
                            map_id text,
                            templar_id text,
                            file text,
                            path text)''', conn=conn)
    # map_gen
    rqlite.execute('''CREATE TABLE IF NOT EXISTS map_gen (
                            id text not null primary key,
                            map_id text,
                            data text)''', conn=conn)

    # map_gen_file - generated files for map
    rqlite.execute('''CREATE TABLE IF NOT EXISTS map_gen_file (
                            id text not null primary key,
                            map_gen_id text,
                            file_map_id text,
                            data text,
                            file text,
                            path text)''', conn=conn)
    logger.info("Database loaded")

def get_mapa(id):
    return rqlite.find_one("select id, name, description from map where id = ?", (id,), fields=["id", "name", "description"])

def get_templars(map_id):
    return rqlite.find("select id, templar_id, file, path from file_map where map_id = ?", (map_id,), fields=["id", "templar_id", "file", "path"])

def find_mapa_by_name(name):
    return rqlite.find('select id, name, description from map where name like ?', ('%'+name+'%',), fields=["id", "name", "description"])

def save_mapa(mapa):
    map_id = str(uuid.uuid4())
    files = [(str(uuid.uuid4()), map_id, f['templar_id'], f['file'], f['path'],) for f in mapa['files']]
    with rqlite.get_closable_connection() as conn:
        rqlite.execute('insert into map (id, name, description) values (?,?,?)', (map_id, mapa['name'], mapa['description'],), conn=conn)
        rqlite.execute_many('''insert into file_map
                               (id, map_id, templar_id, file, path)
                               values (?,?,?,?,?)''', files, conn=conn)
    return map_id

def delete_map(id):
    with rqlite.get_closable_connection() as conn:
        map_gen_ids = rqlite.find('select id from map_gen where map_id = ?', (id,), fields=["id"])
        rqlite.execute('delete map where id = ?', (id,), conn=conn)
        rqlite.execute('delete file_map where map_id = ?', (id,), conn=conn)
        rqlite.execute('delete map_gen where map_id = ?', (id,), conn=conn)
        rqlite.execute('delete map_gen_file where map_gen_id in (?)', (','.join([i['id'] for i in map_gen_ids]),), conn=conn)

def generate_file(map_gen_id, file_map_id):
    id = str(uuid.uuid4())
    with rqlite.get_closable_connection() as conn:
        map_gen = rqlite.find_one('select data from map_gen where id = ?', (map_gen_id,), fields=['data'], conn=conn)
        file_map = rqlite.find_one('select file, path, templar_id from file_map where id = ?', (file_map_id,), fields=['templar_id', 'file', 'path'], conn=conn)

        data = json.loads(map_gen['data'])
        t_content = templar.compile(file_map['templar_id'], data)

        gen = (id, map_gen_id, file_map_id, t_content, file_map['file'], file_map['path'],)
        rqlite.execute('''insert into map_gen_file
                          (id, map_gen_id, file_map_id, data, file, path)
                          values (?,?,?,?,?,?)''', gen, conn=conn)
    return id

def start_map_generation(map_id, data):
    payload = json.dumps(data)
    logger.info("Generation mapa [%s] with [%s]", id, payload)

    gen_id = str(uuid.uuid4())
    files = get_templars(map_id)

    if files is None or len(files) == 0:
        logger.warn("Not found templars for map %s" % map_id)
        return None

    else:
        with rqlite.get_closable_connection() as conn:
            rqlite.execute('''insert into map_gen
                                   (id, map_id, data)
                                   values (?,?,?)''', (gen_id, map_id, payload, ), conn=conn)

        for file in files:
            rabbitmq.publish(exchange, routing_key, {'map_gen_id': gen_id, 'file_map_id': file['id'], 'templar_id': file['templar_id']}, rabbit_conn)

        return gen_id
