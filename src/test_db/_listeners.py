from datetime import datetime, timezone
import logging

# import sqlobject.sqlbuilder  # type: ignore

logger = logging.getLogger(__name__)


def updateListener(instance, kwargs):
    """keep updatedAt field current"""
    # ToDo: in this case it seems to write a fnction to the DB
    # kwargs["updatedAt"] = sqlobject.sqlbuilder.func.strftime(
    #     "%Y-%m-%d %H:%M:%f", "now"
    # )
    kwargs["updatedAt"] = datetime.now(timezone.utc)
