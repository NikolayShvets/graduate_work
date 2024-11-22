from models import UserRole
from repository.base import SQLAlchemyRepository


class UserRoleRepository(SQLAlchemyRepository[UserRole]):
    pass


user_role_repository = UserRoleRepository(UserRole)
