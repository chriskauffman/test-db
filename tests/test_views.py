from datetime import date, datetime

from typeid import TypeID

import test_db
from test_db._views._address import AddressView
from test_db._views._bank_account import BankAccountView
from test_db._views._base_view import BaseView
from test_db._views._debit_card import DebitCardView
from test_db._views._job import JobView
from test_db._views._organization import OrganizationView
from test_db._views._person import PersonView


def test_base_view_input_validation(monkeypatch, capsys):
    inputs = iter(
        [
            "",
            "value",
            "NULL",
            "bad date",
            "01/02/2025",
            "not a number",
            "123",
            "invalid type ID",
            str(TypeID("p")),
        ]
    )
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    assert BaseView._getInput("Required") == "value"
    assert BaseView._getInput("Optional", acceptNull=True) == ""
    assert BaseView._getDateInput("Date").date() == date(2025, 1, 2)
    assert BaseView._getStrInput("Number", numeric=True) == "123"
    assert BaseView._getTypeIDInput("gID").prefix == "p"

    assert "Input is required" in capsys.readouterr().out


def test_entity_views_edit_and_details(monkeypatch, capsys, temporary_db):
    previous_auto_create_dependents = test_db.autoCreateDependents
    test_db.autoCreateDependents = False
    try:
        person = test_db.Person(connection=temporary_db.connection)
        organization = test_db.Organization(connection=temporary_db.connection)
        person_address = test_db.PersonAddress(
            person=person, connection=temporary_db.connection
        )
        organization_address = test_db.OrganizationAddress(
            organization=organization, connection=temporary_db.connection
        )
        person_bank_account = test_db.PersonBankAccount(
            person=person, connection=temporary_db.connection
        )
        organization_bank_account = test_db.OrganizationBankAccount(
            organization=organization, connection=temporary_db.connection
        )
        debit_card = test_db.PersonDebitCard(
            person=person, connection=temporary_db.connection
        )
        job = test_db.Job(
            person=person,
            organization=organization,
            connection=temporary_db.connection,
        )

        monkeypatch.setattr(
            BaseView,
            "_getTypeIDInput",
            staticmethod(lambda prompt, default=None: default),
        )
        monkeypatch.setattr(
            BaseView,
            "_getStrInput",
            staticmethod(
                lambda prompt, default=None, numeric=False, acceptNull=False: (
                    default or "updated"
                )
            ),
        )
        monkeypatch.setattr(
            BaseView,
            "_getDateInput",
            staticmethod(
                lambda prompt, default=None: datetime.strptime(
                    default or "01/02/2025", "%m/%d/%Y"
                ).date()
            ),
        )

        views = (
            PersonView(person),
            OrganizationView(organization),
            AddressView(person_address),
            AddressView(organization_address),
            BankAccountView(person_bank_account),
            BankAccountView(organization_bank_account),
            DebitCardView(debit_card),
            JobView(job),
        )
        for view in views:
            view.edit()
            view.view()
            view.viewDetails()

        output = capsys.readouterr().out
        assert str(person.gID) in output
        assert str(organization.gID) in output
        assert str(job.gID) in output
    finally:
        test_db.autoCreateDependents = previous_auto_create_dependents


def test_person_view_delete_confirmation(monkeypatch, temporary_db):
    previous_auto_create_dependents = test_db.autoCreateDependents
    test_db.autoCreateDependents = False
    try:
        initial_count = test_db.Person.select(
            connection=temporary_db.connection
        ).count()
        person = test_db.Person(connection=temporary_db.connection)
        person_view = PersonView(person)
        monkeypatch.setattr("builtins.input", lambda prompt: "n")
        person_view.delete()
        assert (
            test_db.Person.select(connection=temporary_db.connection).count()
            == initial_count + 1
        )

        monkeypatch.setattr("builtins.input", lambda prompt: "y")
        person_view.delete()
        assert (
            test_db.Person.select(connection=temporary_db.connection).count()
            == initial_count
        )
    finally:
        test_db.autoCreateDependents = previous_auto_create_dependents
