from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgresql import get_async_session

Session = Annotated[AsyncSession, Depends(get_async_session)]
