from typing import TypeVar, Generic, Self
from argparse import ArgumentParser, Namespace
from os import environ
from abc import ABC, abstractmethod
import logging

T = TypeVar('T')


class Option(Generic[T], ABC):
    def __init__(self, parser: ArgumentParser, name: str, default_value: T, env_var_name: str, help_text: str, name_and_flags: list[str]):
        self.parser = parser
        self.name = name
        self.default_value = default_value
        self.env_var_name = env_var_name
        self.help_text = help_text
        self.name_and_flags = name_and_flags
        self._add_argument()

    def value(self, args: Namespace) -> T:
        env_var_value = self._retrieve_env_var_value()
        option_value = self._retrieve_option_value(args)
        if option_value is not None:
            return option_value
        elif env_var_value is not None:
            return env_var_value
        return self.default_value

    @abstractmethod
    def _add_argument(self) -> Self:
        raise NotImplementedError()

    @abstractmethod
    def _validator(self, value: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _parse_value(self, value: str) -> T:
        raise NotImplementedError()

    @abstractmethod
    def _env_var_name_validation_error_message(self, env_var_name: str, value: str) -> str:
        raise NotImplementedError()

    def _retrieve_env_var_value(self) -> T | None:
        # Check env var name is set
        if self.env_var_name is None:
            return None
        # Check env var exists
        if self.env_var_name not in environ:
            return None
        value = environ[self.env_var_name]
        # Check value is valid
        if not self._validator(value):
            logging.error(self._env_var_name_validation_error_message(self.env_var_name, value))
        # Parse and return value
        return self._parse_value(value)

    def _retrieve_option_value(self, args: Namespace) -> T | None:
        value = getattr(args, self.name)
        if value is None or value == '':
            return None
        return value
