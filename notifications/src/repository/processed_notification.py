from models import ProcessedNotifications
from repository.base import SQLAlchemyRepository


class ProcessedNotificationsRepository(SQLAlchemyRepository[ProcessedNotifications]):
    pass


processed_notifications_repository = ProcessedNotificationsRepository(
    ProcessedNotifications
)
