from datetime import datetime, timezone
import logging


logger = logging.getLogger(__name__)


def handleRowCreateSignal(instance, kwargs, post_funcs):
    """Sets createdAt field"""
    kwargs["updatedAt"] = datetime.now(timezone.utc)
    kwargs["createdAt"] = kwargs.get("createdAt") or kwargs["updatedAt"]


def handleRowUpdateSignal(instance, kwargs):
    """Keeps updatedAt field current"""
    kwargs["updatedAt"] = datetime.now(timezone.utc)
