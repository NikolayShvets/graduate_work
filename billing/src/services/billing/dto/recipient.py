from services.billing.dto.base import Base


class Recipient(Base):
    account_id: int
    gateway_id: int
