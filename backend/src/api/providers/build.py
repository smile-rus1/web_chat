from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.files_work.files_manager import FilesManager
from src.infrastructure.files_work.files_work import ImageStorage
from src.services.transaction_manager import TransactionManager
from src.infrastructure.db import repo


def build_tm(
        session: AsyncSession
) -> TransactionManager:
    return TransactionManager(
        session=session,
        account_repo=repo.AccountRepo,
        chat_repo=repo.ChatRepo,
    )


def build_fm(
        base_dir: Path,
        chunk_size: int | None = None
):
    return FilesManager(
        file_storage=ImageStorage(base_dir, chunk_size=chunk_size)
    )
