from models import RefreshToken
from repository.base import SQLAlchemyRepository


class RefreshTokenRepository(SQLAlchemyRepository[RefreshToken]):
    pass


refresh_token_repository = RefreshTokenRepository(RefreshToken)
