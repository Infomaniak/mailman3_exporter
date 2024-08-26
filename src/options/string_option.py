from typing import Self
from src.options.option import Option
from argparse import ArgumentParser


class StringOption(Option[str]):
    def __init__(self, parser: ArgumentParser, name: str, default_value: str, env_var_name: str, help_text: str, name_and_flags: list[str]):
        super().__init__(parser, name, default_value, env_var_name, help_text, name_and_flags)

    def _add_argument(self) -> Self:
        self.parser.add_argument(
            *self.name_and_flags,
            dest=self.name,
            type=str,
            help=self.help_text
        )
        return self

    def _validator(self, value: str) -> bool:
        return True

    def _parse_value(self, value: str) -> str:
        return value

    def _env_var_name_validation_error_message(self, env_var_name: str, value: str) -> str:
        return f"{env_var_name} must be a valid value: {value}"
