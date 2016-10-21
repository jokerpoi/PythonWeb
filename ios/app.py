import logging;

logging.basicConfig(level=logging.INFO)

import asyncio
from aiohttp import web
from Model import *
from Entity import *


def index(request):
    return web.Response(body=b"<h1>Asomeon</h1>", content_type='text/html', charset='UTF-8')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv


loop = asyncio.get_event_loop()


@asyncio.coroutine
def test():
    yield from create_pool(loop=loop, host='localhost', port=3306, user='root', password='123456', db='pythondb')
    u = User(name='bob',email="asdasd@s",password="123456",image="about:blank")
    yield from u.save()
    yield from destory_pool()


loop.run_until_complete(test())
loop.close()
