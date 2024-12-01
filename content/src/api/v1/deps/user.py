from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from clients.auth.client import auth_client
from clients.auth.schemas import UserRetrieveSchema
from settings.api import settings as api_settings
from settings.jwt import settings as jwt_settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{api_settings.AUTH_API_URL}/auth/api/v1/jwt/login",
)


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token,
            jwt_settings.SECRET_KEY,
            jwt_settings.JWT_ALGORITHM,
        )
    except jwt.PyJWTError:
        return None
    except ValueError:
        return None
    return decoded_token


async def check_user(
    token: str = Depends(oauth2_scheme),
) -> UserRetrieveSchema:
    try:
        return await auth_client.check(token)
    except Exception as e:
        data = decode_jwt(token)

        if not data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

        return UserRetrieveSchema(**data)


UserData = Annotated[UserRetrieveSchema, Depends(check_user)]
