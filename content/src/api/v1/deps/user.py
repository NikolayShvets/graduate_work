from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from clients.auth.client import auth_client
from clients.auth.schemas import UserRetrieveSchema
from settings.api import settings as api_settings
from settings.jwt import settings as jwt_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=api_settings.EXTERNAL_LOGIN_URL)


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=jwt_settings.SECRET_KEY.get_secret_value(),
            algorithms=[jwt_settings.ALGORITHM],
            audience=jwt_settings.AUD,
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


async def check_login(credentials) -> UserRetrieveSchema:
    try:
        return await auth_client.login(credentials)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


async def check_admin(token: str):
    is_admin = await auth_client.check_admin(token)
    if not isinstance(is_admin, bool):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )


async def logout(token: str):
    try:
        return await auth_client.logout(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e)


UserData = Annotated[UserRetrieveSchema, Depends(check_user)]
