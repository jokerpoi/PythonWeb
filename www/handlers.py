from dataFactory import *
import asyncio
from Entity import *
from aiohttp import web
from apis import *
from page import Page
' url handlers '

#测试mvc页面
@get('/')
def index(request):
    users = yield from User.findAll()
    return {
        '__template__':'test.html',
        'users' : users
    }

@get("/blogs")
def showBlogs(request):
    user = yield from User.find('oo')
    return {
        '__template__':'blogs.html',
        'user': user
        }

@get("/api/users")
def api_get_users(*, page='1'):
    #获取数据库中拥有的数据条数
    uNum = yield from User.findAll()
    num = len(uNum)
    p = Page(num,page)
    if num == 0:
        return dict(page=p,users=())
    users = yield from User.findByPage(offset=p.pageNo,limit=p.limit)
    for u in users:
        u['password'] = '******'
    return dict(page=p,users=users)