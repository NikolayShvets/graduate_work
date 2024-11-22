from models import User
from repository.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    pass


user_repository = UserRepository(User)
