from models import Transactions
from repository.base import SQLAlchemyRepository


class TransactionRepository(SQLAlchemyRepository[Transactions]):
    pass


transaction_repository = TransactionRepository(Transactions)
