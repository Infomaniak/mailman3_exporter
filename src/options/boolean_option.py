from src.options.choices_option import ChoicesOption
from argparse import ArgumentParser, Namespace

ENABLED_TEXT = 'true'
DISABLED_TEXT = 'false'
BOOLEAN_CHOICES = [ENABLED_TEXT, DISABLED_TEXT]


class BooleanOption(ChoicesOption):
    def __init__(self, parser: ArgumentParser, name: str, default_value: bool, env_var_name: str, help_text: str, name_and_flags: list[str]):
        super().__init__(parser, name, BOOLEAN_CHOICES, str(default_value).lower(), env_var_name, help_text, name_and_flags)

    def value(self, args: Namespace) -> bool:
        return super().value(args) == ENABLED_TEXT
