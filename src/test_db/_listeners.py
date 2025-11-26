from datetime import datetime, timezone
import logging


logger = logging.getLogger(__name__)


def createListener(instance, kwargs, post_funcs):
    """Sets createdAt field"""
    kwargs["createdAt"] = datetime.now(timezone.utc)
    kwargs["updatedAt"] = kwargs["createdAt"]


def updateListener(instance, kwargs):
    """Keeps updatedAt field current"""
    kwargs["updatedAt"] = datetime.now(timezone.utc)
