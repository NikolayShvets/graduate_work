from models import Subscriptions
from repository.base import SQLAlchemyRepository


class SubscriptionRepository(SQLAlchemyRepository[Subscriptions]):
    # async def
    pass


subscription_repository = SubscriptionRepository(Subscriptions)
