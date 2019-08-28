from models import User
from main import session


class User_Ctrl():

    def new_user(self, status):
        return User(
            id=status.id,
            screen_name=status.screen_name,
            created_at=status.created_at,
        )

    def add_user(self, user):
        session.add(user)
        session.commit()

    def add_users(self, user_list):
        for user in user_list:
            session.add(user)
        
        session.commit()