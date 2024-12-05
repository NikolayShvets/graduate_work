from pydantic import HttpUrl

from services.yookassa.dto.base import Base
from services.yookassa.dto.types import ConfirmationType


class Confirmation(Base):
    type: ConfirmationType
    confirmation_url: HttpUrl | None = None
    return_url: HttpUrl
