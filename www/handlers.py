from dataFactory import *
import asyncio
from Entity import *
from aiohttp import web
' url handlers '

#测试mvc页面
@get('/')
def index(request):
    users = yield from User.findAll()
    return {
        '__template__':'test.html',
        'users' : users
    }