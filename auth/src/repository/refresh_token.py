from src.models import RefreshToken
from src.repository.base import SQLAlchemyRepository


class RefreshTokenRepository(SQLAlchemyRepository[RefreshToken]):
    pass


refresh_token_repository = RefreshTokenRepository(RefreshToken)
