from uuid import UUID

from fastapi_users import BaseUserManager, UUIDIDMixin

from models import User
from settings.api import settings as api_settings


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = api_settings.SECRET_KEY
    verification_token_secret = api_settings.SECRET_KEY
