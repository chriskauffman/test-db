from datetime import datetime, timezone
import logging

# import sqlobject.sqlbuilder  # type: ignore

logger = logging.getLogger(__name__)


def update_listener(instance, kwargs):
    """keep last_updated field current"""
    # ToDo: in this case it seems to write a fnction to the DB
    # kwargs["updated_at"] = sqlobject.sqlbuilder.func.strftime(
    #     "%Y-%m-%d %H:%M:%f", "now"
    # )
    kwargs["updated_at"] = datetime.now(timezone.utc)
