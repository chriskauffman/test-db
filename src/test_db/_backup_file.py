import datetime
import logging
import pathlib
import shutil

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

logger = logging.getLogger(__name__)


def backupFile(
    file_path: pathlib.Path, backup_path: pathlib.Path
) -> Optional[pathlib.Path]:
    if file_path.is_file():
        if backup_path.is_dir():
            backup_file_path = pathlib.Path(
                backup_path,
                file_path.with_suffix(
                    f".{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    f"{file_path.suffix}"
                ).name,
            )
            shutil.copy2(
                file_path,
                backup_file_path,
            )
            return backup_file_path
        else:
            raise ValueError(
                f"error: incorrect backup_path {backup_path}, must be existing directory"
            )
    logger.debug("no file to backup at %s", file_path)
    return None
