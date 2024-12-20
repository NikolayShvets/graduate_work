from uuid import UUID

from api.v1.schemas.base import Base


class PersonResponseSchema(Base):
    id: UUID
    full_name: str
