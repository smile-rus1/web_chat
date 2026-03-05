from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyRepo:
    def __init__(self, session: AsyncSession):
        self._session = session
