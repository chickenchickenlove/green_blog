from peewee import Database
from data.domain import User, UserPost


class UserRepository:

    def __init__(self, database: Database):
        self.db = database

    def get_or_create(self, url):
        user, created = User.get_or_create(url=url)
        return user


class UserPostRepository:

    def __init__(self, database: Database):
        self.db = database

    def get_or_create(self, user, posted_date) -> UserPost:
        query = UserPost.select().where((UserPost.user == user) & (UserPost.posted_date == posted_date))
        try:
            return query.get()
        except Exception as _:
            return UserPost.create(user=user, posted_date=posted_date, posted_count=0)

    def save(self, user_post: UserPost):
        user_post.save()


