from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from api.v1.deps.fastapi_users import CurrentUser
from api.v1.deps.session import Session
from models import User, UserRole
from repository.user import user_repository


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self._allowed_roles = allowed_roles

    async def __call__(self, user: CurrentUser, session: Session) -> bool:
        # TODO: туповато, но переопределять методы UserManager из fastapi-users довольно муторно
        user = await user_repository.get(
            session, id=user.id, options=[joinedload(User.roles).joinedload(UserRole.role)]
        )
        role_names = {user_role.role.name for user_role in user.roles}
        print(f'\nin role_checker()')
        print(f'\tuser: {user.email}')
        print(f'\tuser_roles: {role_names}')


        if not role_names.intersection(self._allowed_roles) and not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return True


ForAdminOnly = Annotated[bool, Depends(RoleChecker(allowed_roles=["admin"]))]
