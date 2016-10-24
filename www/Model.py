from ORM import ModelMetaclass
from sqlIDUS import *

import logging;

logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
import aiomysql


# orm映射基类
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return __getattr__(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using defalut value for %s:%s' % (key, str(value)))
        return value

    @classmethod
    async def find(cls, primarykey):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [primarykey], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    @classmethod
    @asyncio.coroutine
    def findAll(cls, **kw):
        rs = []
        if len(kw) == 0:
            rs = yield from select(cls.__select__, None)
        else:
            args = []
            values = []
            for key, value in kw.items():
                args.append('%s=?' % key)
                values.append(value)
            rs = yield from select('where `%s`=?' % (cls.__select__, ' and ', join(key)), values)
        return rs

    @classmethod
    @asyncio.coroutine
    def update(cls,**kw):
        ret = 0 #受影响的行数
        values = []
        primary = kw.get(cls.__primary_key__)
        kw.pop(cls.__primary_key__)
        for key,value in kw.items():
            values.append(value)
        values.append(primary)
        print('update :',cls.__update__,kw.get(cls.__primary_key__))
        ret = yield from execute('%s' % cls.__update__,values)
        return ret

    @classmethod
    @asyncio.coroutine
    def remove(cls,**kw):
        primary = kw.get(cls.__primary_key__)
        ret = yield from execute('%s' % cls.__delete__,primary)
        return ret

