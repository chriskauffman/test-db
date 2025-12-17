import test_db


class _TyperOptions:
    @property
    def interactive(self):
        return test_db.typer.interactive
