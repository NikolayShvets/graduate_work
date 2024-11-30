from models import Role
from repository.base import SQLAlchemyRepository


class RoleRepository(SQLAlchemyRepository[Role]):
    pass


role_repository = RoleRepository(Role)
