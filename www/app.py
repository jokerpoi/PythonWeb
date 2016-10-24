import logging;

logging.basicConfig(level=logging.INFO)

import asyncio,os,json,time
from aiohttp import web
from Model import *
from Entity import *
from dataFactory import *
from handlers import *
from jinja2 import Environment,FileSystemLoader


def init_jinja2(app,**kw):
    logging.info('init jinja2')
    options = dict(
        autoescape = kw.get('autoescape',True),
        block_start_string = kw.get('block_start_string','{%'),
        block_end_string = kw.get('block_end_string','%}'),
        variable_start_string = kw.get('variable_start_string','{{'),
        variable_end_string = kw.get('variable_end_string','}}'),
        auto_reload = kw.get('auto_reload',True)
    )
    path = kw.get('path',None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path),**options)
    filters = kw.get('filters',env)
    if filters is not None:
        for name,f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (yield from handler(request))

    return logger


@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info('Response handler...')
        r = yield from handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(
                    body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp

    return response

@asyncio.coroutine
def init(loop):
    yield from create_pool(loop=loop, host='localhost', port=3306, user='root', password='123456', db='pythondb')
    app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])
    init_jinja2(app,filters=dict(datatime='9996'))
    add_routes(app, 'handlers')
    add_static(app)
    # app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started in http://127.0.0.1:9000')

    return srv


loop = asyncio.get_event_loop()


@asyncio.coroutine
def test():
    u = User(name='bob', email="asdasd@s", password="123456", image="about:blank")
    yield from u.save()
    yield from destory_pool()


loop.run_until_complete(init(loop))
loop.run_forever()
# loop.close()
