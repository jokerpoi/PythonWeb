from ORM import StringField,IntegerField,FloatField,BooleanField
from Model import Model
import time,uuid

def nextId():
    return '%s' % uuid.uuid4().hex

#对应表的实体类

class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True,default=nextId(),ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = IntegerField(default=0) #是否为管理员0-普通，1-admin
    email = StringField(ddl="varchar(50)")
    image = StringField(ddl="varchar(500)")
    created_at =FloatField(default=time.time)#创建时间

class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=nextId(), ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl="varchar(500)")
    content = StringField(ddl="varchar(700)")
    name = StringField(ddl="varchar(200)")
    summary = StringField(ddl="varchar(200)") #小结
    created_at = FloatField(default=time.time)  # 创建时间

class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=nextId(), ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl="varchar(500)")
    blog_id = StringField(ddl='varchar(50)')
    content = StringField(ddl="varchar(700)")
    created_at = FloatField(default=time.time)  # 创建时间


