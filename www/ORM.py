import logging;

logging.basicConfig(level=logging.INFO)


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s,%s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class IntegerField(Field):
    """docstring for IntegerField"""

    def __init__(self, name=None, primary_key=False, default=None, ddl='bigint'):
        super().__init__(name, ddl, primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='real'):
        super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='bool'):
        super().__init__(name, ddl, primary_key, default)

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ','.join(L)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        # 获取table名称
        tableName = attrs.get('__table__', None) or name
        logging.info('found model:%s(table:%s)' % (name, tableName))
        # 获取所有的Field和主键名:
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info(' found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键
                    if primary_key:
                        raise RuntimeError("Duplicate primary key of field: %s" % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '%s' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__tabel__'] = tableName
        attrs['__primary_key__'] = primaryKey  # 主键属性名
        attrs['__fields__'] = fields  # 除主键外的属性名
        # 构造默认的select,insert,update,delete语句:
        attrs['__select__'] = 'select `%s`,%s from `%s`' % (primaryKey, ','.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s`(%s,`%s`) values(%s)' % (tableName, ','.join(escaped_fields),
                                                                        primaryKey,
                                                                        create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?' % (tableName,
                                                                     ','.join(map(lambda f: '`%s`=?' % (
                                                                     mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)
