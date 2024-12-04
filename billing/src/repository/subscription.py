from models import Subscriptions
from repository.base import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository[Subscriptions]):
    pass


subscription_repository = SubscriptionRepository(Subscriptions)
