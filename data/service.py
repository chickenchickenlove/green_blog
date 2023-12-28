from data.domain import User, UserPost
from data.repository import UserRepository, UserPostRepository


class UserPostService:

    def __init__(self,
                 user_repository: UserRepository,
                 user_post_repository: UserPostRepository):
        self.user_repository = user_repository
        self.user_post_repository = user_post_repository

    def update_record(self, url, records):
        user = self.user_repository.get_or_create(url)

        for posted_date, count in records.items():
            user_post = self.user_post_repository.get_or_create(user, posted_date)

            user_post.posted_date = posted_date
            user_post.posted_count = count

            self.user_post_repository.save(user_post)