from uuid import UUID as PY_UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from schemas.notification import DeliveryMethod, EventType


class ProcessedNotifications(Base):
    notification_id: Mapped[PY_UUID] = mapped_column(UUID, index=True)

    def __str__(self):
        return f"{self.notification_id} processed at {self.created_at}"


class EventTypes(Base):
    type: Mapped[EventType] = mapped_column(
        ENUM(EventType, name="event_type"),
        unique=True,
    )
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    notification_templates: Mapped["NotificationTemplates"] = relationship(
        "NotificationTemplates", back_populates="event_type"
    )

    def __str__(self):
        return f"Event type ({self.id}) {self.type}"


class DeliveryMethods(Base):
    method: Mapped[DeliveryMethod] = mapped_column(
        ENUM(DeliveryMethod, name="delivery_method"),
        unique=True,
    )
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    notification_templates: Mapped["NotificationTemplates"] = relationship(
        "NotificationTemplates", back_populates="delivery_method"
    )

    def __str__(self):
        return f"Delivery method ({self.id}) {self.method}"


class Templates(Base):
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(32))
    template: Mapped[str] = mapped_column(Text, unique=True)

    notification_templates: Mapped["NotificationTemplates"] = relationship(
        "NotificationTemplates", back_populates="template"
    )

    def __str__(self):
        return f"Template ({self.id}) {self.subject}"

    def __repr__(self):
        return self.template


class NotificationTemplates(Base):
    __table_args__ = (
        UniqueConstraint(
            "event_type_id",
            "delivery_method_id",
            name="uq_event_delivery_method",
        ),
    )

    event_type_id: Mapped[PY_UUID] = mapped_column(ForeignKey("eventtypes.id"))
    delivery_method_id: Mapped[PY_UUID] = mapped_column(
        ForeignKey("deliverymethods.id")
    )
    template_id: Mapped[PY_UUID] = mapped_column(ForeignKey("templates.id"))

    event_type: Mapped[EventTypes] = relationship(
        "EventTypes", back_populates="notification_templates"
    )
    delivery_method: Mapped[DeliveryMethods] = relationship(
        "DeliveryMethods", back_populates="notification_templates"
    )
    template: Mapped[Templates] = relationship(
        "Templates", back_populates="notification_templates"
    )

    def __str__(self):
        return (
            f"Notification template ({self.id}) "
            f"{self.event_type} {self.delivery_method}"
        )
