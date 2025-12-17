import sys

from formencode.validators import Invalid  # type: ignore
from sqlobject import SQLObjectNotFound  # type: ignore
import typer
from typing_extensions import Optional

import test_db
from ._typer_options import _TyperOptions
from ._validate import validate_organization, validate_person

job_app = typer.Typer()


def validate_job(gid: str):
    try:
        return test_db.Job.byGID(gid)
    except (Invalid, SQLObjectNotFound) as exc:
        sys.stderr.write(f"error: {str(exc)}")
        sys.exit(1)


@job_app.command("add")
def job_add(organization_gid: Optional[str] = None, person_gid: Optional[str] = None):
    organization = None
    person = None
    if organization_gid:
        organization = validate_organization(organization_gid)
    if person_gid:
        person = validate_person(person_gid)
    test_db.JobView.add(
        organization=organization,
        person=person,
        interactive=_TyperOptions().interactive,
    )


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
