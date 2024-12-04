from pydantic import HttpUrl

from services.billing.dto.base import Base
from services.billing.dto.types import ConfirmationType


class Confirmation(Base):
    type: ConfirmationType
    return_url: HttpUrl
