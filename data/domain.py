from peewee import MySQLDatabase
from peewee import Model, CharField, IntegerField, BigAutoField, ForeignKeyField, BooleanField, DateField

# docker
name = 'green_blog'
user = 'green'
password = '1234'
host = '127.0.0.1'
port = 3306
db = MySQLDatabase(name,
                   user=user,
                   password=password,
                   host=host,
                   port=port)


class User(Model):
    user_id = BigAutoField()
    url = CharField(unique=True)
    deleted = BooleanField()

    class Meta:
        database = db


class UserPost(Model):
    user_post_id = BigAutoField()
    user = ForeignKeyField(User, backref='posts')
    posted_date = DateField()
    posted_count = IntegerField()

    class Meta:
        database = db

        indexes = (
            (('user', 'posted_date'), True),
        )


db.connect()
db.create_tables([User, UserPost], safe=True)
print('here')