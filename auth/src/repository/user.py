from src.models import User
from src.repository.base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    pass


user_repository = UserRepository(User)
