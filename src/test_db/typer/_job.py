import logging

import typer

# Using typing_extensions vs typing:
# https://stackoverflow.com/questions/71944041/using-modern-typing-features-on-older-versions-of-python
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_job, validate_organization, validate_person

logger = logging.getLogger(__name__)

job_app = typer.Typer()


@job_app.command("add")
def job_add(organization_gid: Optional[str] = None, person_gid: Optional[str] = None):
    organization = None
    person = None
    if organization_gid:
        organization = validate_organization(organization_gid)
    if person_gid:
        person = validate_person(person_gid)
    job = test_db.Job(
        organization=organization,
        person=person,
    )
    if _TyperOptions().interactive:
        test_db.JobView(job).edit()
    print(job.gID)


@job_app.command("delete")
def job_delete(gid: str):
    job = validate_job(gid)
    job.destroySelf()


@job_app.command("edit")
def job_edit(gid: str):
    job = validate_job(gid)
    test_db.JobView(job).edit()


@job_app.command("list")
def job_list():
    test_db.JobView.list()


@job_app.command("view")
def job_view(gid: str):
    job = validate_job(gid)
    test_db.JobView(job).viewDetails()
