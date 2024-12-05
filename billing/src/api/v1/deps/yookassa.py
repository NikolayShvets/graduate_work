from typing import Annotated

from fastapi import Depends

from services.yookassa.service import YooKassa as _YooKassa


def get_yookassa_service() -> _YooKassa:
    return _YooKassa()


YooKassa = Annotated[_YooKassa, Depends(get_yookassa_service)]
