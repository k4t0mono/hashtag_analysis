from models import User
from main import session, logger


class User_Ctrl():

    def new_user(self, user_):
        return User(
            id=user_.id,
            screen_name=user_.screen_name,
            created_at=user_.created_at,
        )

    def add_user(self, user):
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            logger.debug(e)
            session.rollback()
        else:
            logger.info("Added user {}:{}".format(user.id, user.screen_name))

    def add_users(self, user_list):
        for user in user_list:
            if self.get_user(user.id):
                continue

            session.add(user)
        
        session.commit()

    def get_user(self, id_):
        try:
            return session.query(User).filter(User.id == id_).one()
        except:
            return None