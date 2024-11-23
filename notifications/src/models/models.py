from uuid import UUID as PY_UUID

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ProcessedNotifications(Base):
    notification_id: Mapped[PY_UUID] = mapped_column(UUID, index=True)

    def __str__(self):
        return f"{self.notification_id} processed at {self.created_at}"
