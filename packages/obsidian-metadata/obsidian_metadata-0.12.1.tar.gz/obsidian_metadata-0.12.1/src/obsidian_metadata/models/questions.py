"""Functions for asking questions to the user and validating responses.

This module contains wrappers around questionary to ask questions to the user and validate responses. Mocking questionary has proven very difficult. This functionality is separated from the main application logic to make it easier to test.

Progress towards testing questionary can be found on this issue:
https://github.com/tmbo/questionary/issues/35
"""
import re
from pathlib import Path
from typing import Any

import questionary
import typer

from obsidian_metadata.models.enums import InsertLocation, MetadataType
from obsidian_metadata.models.parsers import Parser
from obsidian_metadata.models.vault import Vault

P = Parser()

# Reset the default style of the questionary prompts qmark
questionary.prompts.checkbox.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.common.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.confirm.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.confirm.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.path.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.select.DEFAULT_STYLE = questionary.Style([("qmark", "")])
questionary.prompts.text.DEFAULT_STYLE = questionary.Style([("qmark", "")])


class Questions:
    """Class for asking questions to the user and validating responses with questionary."""

    @staticmethod
    def ask_for_vault_path() -> Path:  # pragma: no cover
        """Ask the user for the path to their vault.

        Returns:
            Path: The path to the vault.
        """
        vault_path = questionary.path(
            "Enter a path to Obsidian vault:",
            only_directories=True,
            validate=Questions._validate_valid_dir,
        ).ask()
        if vault_path is None:
            raise typer.Exit(code=1)

        return Path(vault_path).expanduser().resolve()

    @staticmethod
    def _validate_valid_dir(path: str) -> bool | str:
        """Validate a valid directory.

        Returns:
            bool | str: True if the path is valid, otherwise a string with the error message.
        """
        path_to_validate: Path = Path(path).expanduser().resolve()
        if not path_to_validate.exists():
            return f"Path does not exist: {path_to_validate}"
        if not path_to_validate.is_dir():
            return f"Path is not a directory: {path_to_validate}"

        return True

    def __init__(self, vault: Vault = None, key: str | None = None) -> None:
        """Initialize the class.

        Args:
            vault_path (Path, optional): The path to the vault. Defaults to None.
            vault (Vault, optional): The vault object. Defaults to None.
            key (str, optional): The key to use when validating a key, value pair. Defaults to None.
        """
        self.style = questionary.Style(
            [
                ("qmark", "bold"),
                ("question", "bold"),
                ("separator", "fg:#808080"),
                ("answer", "fg:#FF9D00 bold"),
                ("instruction", "fg:#808080"),
                ("highlighted", "bold underline"),
                ("text", ""),
                ("pointer", "bold"),
            ]
        )
        self.vault = vault
        self.key = key

    def _validate_existing_tag(self, text: str) -> bool | str:
        """Validate an existing inline tag.

        Returns:
            bool | str: True if the tag is valid, otherwise a string with the error message.
        """
        if len(text) < 1:
            return "Tag cannot be empty"

        if not self.vault.contains_metadata(meta_type=MetadataType.TAGS, key=None, value=text):
            return f"'{text}' does not exist as a tag in the vault"

        return True

    def _validate_key_exists(self, text: str) -> bool | str:
        """Validate a valid key.

        Returns:
            bool | str: True if the key is valid, otherwise a string with the error message.
        """
        if len(text) < 1:
            return "Key cannot be empty"

        if not self.vault.contains_metadata(meta_type=MetadataType.META, key=text):
            return f"'{text}' does not exist as a key in the vault"

        return True

    def _validate_key_exists_regex(self, text: str) -> bool | str:
        """Validate a valid key.

        Returns:
            bool | str: True if the key is valid, otherwise a string with the error message.
        """
        if len(text) < 1:
            return "Key cannot be empty"

        try:
            re.compile(text)
        except re.error as error:
            return f"Invalid regex: {error}"

        if not self.vault.contains_metadata(meta_type=MetadataType.META, key=text, is_regex=True):
            return f"'{text}' does not exist as a key in the vault"

        return True

    def _validate_new_key(self, text: str) -> bool | str:
        """Validate the tag name.

        Args:
            text (str): The key name to validate.

        Returns:
            bool | str: True if the key is valid, otherwise a string with the error message.
        """
        if P.validate_key_text.search(text) is not None:
            return "Key cannot contain spaces or special characters"

        if len(text) == 0:
            return "New key cannot be empty"

        return True

    def _validate_new_tag(self, text: str) -> bool | str:
        """Validate the tag name.

        Args:
            text (str): The tag name to validate.

        Returns:
            bool | str: True if the tag is valid, otherwise a string with the error message.
        """
        if P.validate_tag_text.search(text) is not None:
            return "Tag cannot contain spaces or special characters"

        if len(text) == 0:
            return "New tag cannot be empty"

        return True

    def _validate_new_value(self, text: str) -> bool | str:
        """Validate a new value.

        Args:
            text (str): The value to validate.

        Returns:
            bool | str: True if the value is valid, otherwise a string with the error message.
        """
        if len(text) < 1:
            return "Value cannot be empty"

        if self.key is not None and self.vault.contains_metadata(
            meta_type=MetadataType.ALL, key=self.key, value=text
        ):
            return f"{self.key}:{text} already exists"

        return True

    def _validate_number(self, text: str) -> bool | str:
        """Validate a number.

        Args:
            text (str): The number to validate.

        Returns:
            bool | str: True if the number is valid, otherwise a string with the error message.
        """
        if not text.isdigit():
            return "Must be an integer"

        return True

    def _validate_path_is_file(self, text: str) -> bool | str:
        """Validate a path is a file.

        Args:
            text (str): The path to validate.

        Returns:
            bool | str: True if the path is valid, otherwise a string with the error message.
        """
        path_to_validate: Path = Path(text).expanduser().resolve()
        if not path_to_validate.exists():
            return f"Path does not exist: {path_to_validate}"
        if not path_to_validate.is_file():
            return f"Path is not a file: {path_to_validate}"

        return True

    def _validate_valid_vault_regex(self, text: str) -> bool | str:
        """Validate a valid regex.

        Returns:
            bool | str: True if the regex is valid, otherwise a string with the error message.
        """
        try:
            re.compile(text)
        except re.error as error:
            return f"Invalid regex: {error}"

        if self.vault is not None:
            for subdir in list(self.vault.vault_path.glob("**/*")):
                if re.search(text, str(subdir)):
                    return True
            return "Regex does not match paths in the vault"

        return True

    def _validate_value(self, text: str) -> bool | str:
        """Validate the value.

        Args:
            text (str): The value to validate.

        Returns:
            bool | str: True if the value is valid, otherwise a string with the error message.
        """
        if len(text) == 0:
            return True

        if self.key is not None and not self.vault.contains_metadata(
            meta_type=MetadataType.ALL, key=self.key, value=text
        ):
            return f"{self.key}:{text} does not exist"

        return True

    def _validate_value_exists_regex(self, text: str) -> bool | str:
        """Validate the value.

        Args:
            text (str): The value to validate.

        Returns:
            bool | str: True if the value is valid, otherwise a string with the error message.
        """
        if len(text) < 1:
            return "Regex cannot be empty"

        try:
            re.compile(text)
        except re.error as error:
            return f"Invalid regex: {error}"

        if self.key is not None and not self.vault.contains_metadata(
            meta_type=MetadataType.ALL, key=self.key, value=text, is_regex=True
        ):
            return f"No values in {self.key} match regex: {text}"

        return True

    def ask_application_main(self) -> str:  # pragma: no cover
        """List for the main application interface.

        Args:
            style (questionary.Style): The style to use for the question.

        Returns:
            str: The selected application.
        """
        return questionary.select(
            "What do you want to do?",
            choices=[
                questionary.Separator("-------------------------------"),
                {"name": "Vault Actions", "value": "vault_actions"},
                {"name": "Export Metadata", "value": "export_metadata"},
                {"name": "Inspect Metadata", "value": "inspect_metadata"},
                {"name": "Filter Notes in Scope", "value": "filter_notes"},
                questionary.Separator("-------------------------------"),
                {"name": "Import bulk changes from CSV", "value": "import_from_csv"},
                {"name": "Add Metadata", "value": "add_metadata"},
                {"name": "Delete Metadata", "value": "delete_metadata"},
                {"name": "Rename Metadata", "value": "rename_metadata"},
                {"name": "Reorganize Metadata", "value": "reorganize_metadata"},
                questionary.Separator("-------------------------------"),
                {"name": "Review Changes", "value": "review_changes"},
                {"name": "Commit Changes", "value": "commit_changes"},
                questionary.Separator("-------------------------------"),
                {"name": "Quit", "value": "abort"},
            ],
            use_shortcuts=False,
            style=self.style,
            qmark="INPUT    |",
        ).ask()

    def ask_confirm(self, question: str, default: bool = True) -> bool:  # pragma: no cover
        """Ask the user to confirm an action.

        Args:
            question (str): The question to ask.
            default (bool, optional): The default value. Defaults to True.

        Returns:
            bool: True if the user confirms, otherwise False.
        """
        return questionary.confirm(
            question, default=default, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_existing_tag(self, question: str = "Enter a tag") -> str:  # pragma: no cover
        """Ask the user for an existing inline tag."""
        return questionary.text(
            question,
            validate=self._validate_existing_tag,
            style=self.style,
            qmark="INPUT    |",
        ).ask()

    def ask_existing_key(self, question: str = "Enter a key") -> str:  # pragma: no cover
        """Ask the user for a metadata key.

        Args:
            question (str, optional): The question to ask. Defaults to "Enter a key".

        Returns:
            str: A metadata key that exists in the vault.
        """
        return questionary.text(
            question, validate=self._validate_key_exists, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_existing_keys_regex(self, question: str = "Regex for keys") -> str:  # pragma: no cover
        """Ask the user for a regex for metadata keys.

        Args:
            question (str, optional): The question to ask. Defaults to "Regex for keys".

        Returns:
            str: A regex for metadata keys that exist in the vault.
        """
        return questionary.text(
            question, validate=self._validate_key_exists_regex, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_existing_value(self, question: str = "Enter a value") -> str:  # pragma: no cover
        """Ask the user for a metadata value.

        Args:
            question (str, optional): The question to ask. Defaults to "Enter a value".

        Returns:
            str: A metadata value.
        """
        return questionary.text(
            question, validate=self._validate_value, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_filter_path(self) -> str:  # pragma: no cover
        """Ask the user for the path to the filter file.

        Returns:
            str: The regex to use for filtering.
        """
        filter_path_regex = questionary.path(
            "Regex to filter the notes being processed by their path:",
            only_directories=False,
            validate=self._validate_valid_vault_regex,
            style=self.style,
            qmark="INPUT    |",
        ).ask()
        if filter_path_regex is None:
            raise typer.Exit(code=1)

        return filter_path_regex

    def ask_existing_value_regex(
        self, question: str = "Regex for values"
    ) -> str:  # pragma: no cover
        """Ask the user for a regex for metadata values.

        Args:
            question (str, optional): The question to ask. Defaults to "Regex for values".

        Returns:
            str: A regex for metadata values that exist in the vault.
        """
        return questionary.text(
            question,
            validate=self._validate_value_exists_regex,
            style=self.style,
            qmark="INPUT    |",
        ).ask()

    def ask_metadata_location(
        self, question: str = "Where in a note should we add metadata"
    ) -> InsertLocation:  # pragma: no cover
        """Ask the user for the location within a note to place new metadata.

        Returns:
            InsertLocation: The location within a note to place new metadata.
        """
        choices = []
        for metadata_location in InsertLocation:
            choices.append({"name": metadata_location.value, "value": metadata_location})

        return self.ask_selection(
            choices=choices,
            question=question,
        )

    def ask_meta_type(self) -> MetadataType | str:  # pragma: no cover
        """Ask the user for the type of metadata to work on.

        Returns:
            MetadataType: The metadata type
        """
        choices = []
        for meta_type in MetadataType:
            match meta_type:
                case MetadataType.ALL | MetadataType.META | MetadataType.KEYS:
                    continue
                case _:
                    choices.append({"name": meta_type.value, "value": meta_type})

        choices.append(questionary.Separator())  # type: ignore [arg-type]
        choices.append({"name": "Cancel", "value": "cancel"})
        return self.ask_selection(
            choices=choices,
            question="Select the type of metadata",
        )

    def ask_new_key(self, question: str = "New key name") -> str:  # pragma: no cover
        """Ask the user for a new metadata key.

        Args:
            question (str, optional): The question to ask. Defaults to "New key name".

        Returns:
            str: A new metadata key.
        """
        return questionary.text(
            question, validate=self._validate_new_key, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_new_tag(self, question: str = "Enter a new tag") -> str:  # pragma: no cover
        """Ask the user for a new tag.

        Args:
            question (str, optional): The question to ask. Defaults to "Enter a new tag".
        """
        return questionary.text(
            question, validate=self._validate_new_tag, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_new_value(self, question: str = "New value") -> str:  # pragma: no cover
        """Ask the user for a new metadata value.

        Args:
            question (str, optional): The question to ask. Defaults to "New value".

        Returns:
            str: A new metadata value.
        """
        return questionary.text(
            question, validate=self._validate_new_value, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_number(self, question: str = "Enter a number") -> int:  # pragma: no cover
        """Ask the user for a number.

        Args:
            question (str, optional): The question to ask. Defaults to "Enter a number".

        Returns:
            int: A number.
        """
        return questionary.text(
            question, validate=self._validate_number, style=self.style, qmark="INPUT    |"
        ).ask()

    def ask_path(
        self, question: str = "Enter a path", valid_file: bool = False
    ) -> str:  # pragma: no cover
        """Ask the user for a path.

        Args:
            question (str, optional): The question to ask. Defaults to "Enter a path".
            valid_file (bool, optional): Whether the path should be a valid file. Defaults to False.

        Returns:
            str: A path.
        """
        if valid_file:
            return questionary.path(
                question,
                only_directories=False,
                style=self.style,
                validate=self._validate_path_is_file,
                qmark="INPUT    |",
            ).ask()

        return questionary.path(question, style=self.style, qmark="INPUT    |").ask()

    def ask_selection(
        self, choices: list[Any], question: str = "Select an option"
    ) -> Any:  # pragma: no cover
        """Ask the user to select an item from a list.

        Args:
            question (str, optional): The question to ask. Defaults to "Select an option".
            choices (list[Any]): The list of choices.

        Returns:
            any: The selected item value.
        """
        return questionary.select(
            question,
            choices=choices,
            use_shortcuts=False,
            style=self.style,
            qmark="INPUT    |",
        ).ask()
