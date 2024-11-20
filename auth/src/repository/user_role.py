from src.models import UserRole
from src.repository.base import SQLAlchemyRepository


class UserRoleRepository(SQLAlchemyRepository[UserRole]):
    pass


user_role_repository = UserRoleRepository(UserRole)
