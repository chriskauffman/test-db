from cmd2 import CommandSet, with_default_category


@with_default_category("Database")
class BaseCommandSet(CommandSet):
    pass
