import logging;

logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime
import aiomysql


async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    # 创建数据库连接
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )


@asyncio.coroutine
def destory_pool():
    global __pool
    if __pool is not None:
        __pool.close()
        yield from __pool.wait_closed()


# #Select
async def select(sql, args=None, size=None):
    print('select:', sql, args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        conn.close()
        return rs


# 数据库IDU操作
async def execute(sql, args):
    print('execute:', sql)
    global __pool
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args or ())
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected
