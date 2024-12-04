from models import Tariffs
from repository.base import SQLAlchemyRepository


class TariffRepository(SQLAlchemyRepository[Tariffs]):
    pass


tariff_repository = TariffRepository(Tariffs)
