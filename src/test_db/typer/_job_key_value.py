import logging
import sys

from sqlobject.dberrors import DuplicateEntryError  # type: ignore
import typer

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_job

logger = logging.getLogger(__name__)

job_key_value_app = typer.Typer()


@job_key_value_app.command("add")
def job_key_value_add(job_gid: str, key: str, value: str):
    job = validate_job(job_gid)
    try:
        key_value = job.getKeyValueByKey(key, value=value)
        if _TyperOptions().interactive:
            test_db.KeyValueView(key_value).edit()
    except DuplicateEntryError as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@job_key_value_app.command("delete")
def job_key_value_delete(job_gid: str, key: str):
    job = validate_job(job_gid)
    key_value = job.getKeyValueByKey(key)
    if key_value:
        key_value.destroySelf()


@job_key_value_app.command("edit")
def key_value_edit(job_gid: str, key: str):
    job = validate_job(job_gid)
    key_value = job.getKeyValueByKey(key)
    test_db.KeyValueView(key_value).edit()


@job_key_value_app.command("list")
def job_key_value_list(job_gid: str):
    job = validate_job(job_gid)
    test_db.KeyValueView.list(job.keyValues)


@job_key_value_app.command("view")
def job_key_value_view(job_gid: str, key: str):
    job = validate_job(job_gid)
    # ToDo: Needs fix: key will always exist
    key_value = job.getKeyValueByKey(key)
    if key_value:
        test_db.KeyValueView(key_value).viewDetails()
