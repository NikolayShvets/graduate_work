from src.models import Role
from src.repository.base import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository[Role]):
    pass


role_repository = RoleRepository(Role)
