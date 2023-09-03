"""Obsidian vault representation."""

import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import rich.repr
import typer
from rich import box
from rich.columns import Columns
from rich.prompt import Confirm
from rich.table import Table

from obsidian_metadata._config.config import VaultConfig
from obsidian_metadata._utils import alerts, dict_contains, merge_dictionaries
from obsidian_metadata._utils.alerts import logger as log
from obsidian_metadata._utils.console import console, console_no_markup
from obsidian_metadata.models import InsertLocation, MetadataType, Note


@dataclass
class VaultFilter:
    """Vault filters."""

    path_filter: str = None
    key_filter: str = None
    value_filter: str = None
    tag_filter: str = None


@rich.repr.auto
class Vault:
    """Representation of the Obsidian vault.

    Attributes:
        vault (Path): Path to the vault.
        dry_run (bool): Whether to perform a dry run.
        backup_path (Path): Path to the backup of the vault.
        notes (list[Note]): List of all notes in the vault.
    """

    def __init__(
        self,
        config: VaultConfig,
        dry_run: bool = False,
        filters: list[VaultFilter] = [],
    ) -> None:
        self.config = config.config
        self.vault_path: Path = config.path
        self.name = self.vault_path.name
        self.insert_location: InsertLocation = self._find_insert_location()
        self.dry_run: bool = dry_run
        self.backup_path: Path = self.vault_path.parent / f"{self.vault_path.name}.bak"
        self.frontmatter: dict[str, list[str]] = {}
        self.inline_meta: dict[str, list[str]] = {}
        self.tags: list[str] = []
        self.exclude_paths: list[Path] = []

        for p in config.exclude_paths:
            self.exclude_paths.append(Path(self.vault_path / p))

        self.filters = filters
        self.all_note_paths = self._find_markdown_notes()

        with console.status(
            "Processing notes...  [dim](Can take a while for a large vault)[/]",
            spinner="bouncingBall",
        ):
            self.all_notes: list[Note] = [
                Note(note_path=p, dry_run=self.dry_run) for p in self.all_note_paths
            ]
            self.notes_in_scope = self._filter_notes()

        self._rebuild_vault_metadata()

    def __rich_repr__(self) -> rich.repr.Result:  # pragma: no cover
        """Define rich representation of Vault."""
        yield "backup_path", self.backup_path
        yield "config", self.config
        yield "dry_run", self.dry_run
        yield "exclude_paths", self.exclude_paths
        yield "filters", self.filters
        yield "insert_location", self.insert_location
        yield "name", self.name
        yield "num_notes_in_scope", len(self.notes_in_scope)
        yield "num_notes", len(self.all_notes)
        yield "vault_path", self.vault_path

    def _filter_notes(self) -> list[Note]:
        """Filter notes by path and metadata using the filters defined in self.filters.

        Returns:
            list[Note]: List of notes matching the filters.
        """
        notes_list = self.all_notes.copy()

        for _filter in self.filters:
            if _filter.path_filter is not None:
                notes_list = [
                    n
                    for n in notes_list
                    if re.search(_filter.path_filter, str(n.note_path.relative_to(self.vault_path)))
                ]

            if _filter.tag_filter is not None:
                notes_list = [
                    n
                    for n in notes_list
                    if n.contains_metadata(
                        MetadataType.TAGS, search_key="", search_value=_filter.tag_filter
                    )
                ]

            if _filter.key_filter is not None and _filter.value_filter is not None:
                notes_list = [
                    n
                    for n in notes_list
                    if n.contains_metadata(
                        meta_type=MetadataType.META,
                        search_key=_filter.key_filter,
                        search_value=_filter.value_filter,
                    )
                ]

            if _filter.key_filter is not None and _filter.value_filter is None:
                notes_list = [
                    n
                    for n in notes_list
                    if n.contains_metadata(
                        MetadataType.META, search_key=_filter.key_filter, search_value=None
                    )
                ]

        return notes_list

    def _find_insert_location(self) -> InsertLocation:
        """Find the insert location for a note from the configuration file.

        Returns:
            InsertLocation: Insert location for the note.
        """
        if self.config["insert_location"].upper() == "TOP":
            return InsertLocation.TOP

        if self.config["insert_location"].upper() == "AFTER_TITLE":
            return InsertLocation.AFTER_TITLE

        if self.config["insert_location"].upper() == "BOTTOM":
            return InsertLocation.BOTTOM

        return InsertLocation.BOTTOM

    @property
    def insert_location(self) -> InsertLocation:
        """Location to insert new or reorganized metadata.

        Returns:
            InsertLocation: The insert location.
        """
        return self._insert_location

    @insert_location.setter
    def insert_location(self, value: InsertLocation) -> None:
        """Set the insert location for the vault.

        Args:
            value (InsertLocation): The insert location to set.
        """
        self._insert_location = value

    def _find_markdown_notes(self) -> list[Path]:
        """Build list of all markdown files in the vault.

        Returns:
            list[Path]: List of paths to all matching files in the vault.

        """
        return [
            p.resolve()
            for p in self.vault_path.glob("**/*")
            if p.suffix in [".md", ".MD", ".markdown", ".MARKDOWN"]
            and not any(item in p.parents for item in self.exclude_paths)
        ]

    def _rebuild_vault_metadata(self) -> None:
        """Rebuild vault metadata. Indexes all frontmatter, inline metadata, and tags and adds them to dictionary objects."""
        with console.status(
            "Processing notes...  [dim](Can take a while for a large vault)[/]",
            spinner="bouncingBall",
        ):
            vault_frontmatter = {}
            vault_inline_meta = {}
            vault_tags = []
            for _note in self.notes_in_scope:
                for field in _note.metadata:
                    match field.meta_type:
                        case MetadataType.FRONTMATTER:
                            if field.clean_key not in vault_frontmatter:
                                vault_frontmatter[field.clean_key] = (
                                    [field.normalized_value]
                                    if field.normalized_value != "-"
                                    else []
                                )
                            elif field.normalized_value != "-":
                                vault_frontmatter[field.clean_key].append(field.normalized_value)
                        case MetadataType.INLINE:
                            if field.clean_key not in vault_inline_meta:
                                vault_inline_meta[field.clean_key] = (
                                    [field.normalized_value]
                                    if field.normalized_value != "-"
                                    else []
                                )
                            elif field.normalized_value != "-":
                                vault_inline_meta[field.clean_key].append(field.normalized_value)
                        case MetadataType.TAGS:
                            if field.normalized_value not in vault_tags:
                                vault_tags.append(field.normalized_value)

            self.frontmatter = {
                k: sorted(list(set(v))) for k, v in sorted(vault_frontmatter.items())
            }
            self.inline_meta = {
                k: sorted(list(set(v))) for k, v in sorted(vault_inline_meta.items())
            }
            self.tags = sorted(list(set(vault_tags)))

    def add_metadata(
        self,
        meta_type: MetadataType,
        key: str | None = None,
        value: str | None = None,
        location: InsertLocation = None,
    ) -> int:
        """Add metadata to all notes in the vault which do not already contain it.

        Args:
            meta_type (MetadataType): Area of metadata to add to.
            key (str): Key to add.
            value (str, optional): Value to add.
            location (InsertLocation, optional): Location to insert metadata. (Defaults to `vault.config.insert_location`)

        Returns:
            int: Number of notes updated.
        """
        if location is None:
            location = self.insert_location

        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.add_metadata(
                meta_type=meta_type, added_key=key, added_value=value, location=location
            ):
                log.trace(f"Added metadata to {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def backup(self) -> None:
        """Backup the vault."""
        log.debug("Backing up vault")
        if self.dry_run:
            alerts.dryrun(f"Backup up vault to: {self.backup_path}")
            console.print("\n")
            return

        try:
            shutil.copytree(self.vault_path, self.backup_path)

        except FileExistsError:  # pragma: no cover
            log.debug("Backup already exists")
            if not Confirm.ask("Vault backup already exists. Overwrite?"):
                alerts.info("Exiting backup not overwritten.")
                return

            log.debug("Overwriting backup")
            shutil.rmtree(self.backup_path)
            shutil.copytree(self.vault_path, self.backup_path)

        alerts.success(f"Vault backed up to: {self.backup_path}")

    def commit_changes(self) -> None:
        """Commit changes by writing to disk."""
        log.debug("Writing changes to vault...")
        if self.dry_run:
            for _note in self.notes_in_scope:
                if _note.has_changes():
                    alerts.dryrun(
                        f"writing changes to {_note.note_path.relative_to(self.vault_path)}"
                    )
            return

        for _note in self.notes_in_scope:
            if _note.has_changes():
                log.trace(f"writing to {_note.note_path}")
                _note.commit()

    def contains_metadata(
        self, meta_type: MetadataType, key: str, value: str | None = None, is_regex: bool = False
    ) -> bool:
        """Check if the vault contains metadata.

        Args:
            meta_type (MetadataType): Area of metadata to check.
            key (str): Key to check.
            value (str, optional): Value to check. Defaults to None.
            is_regex (bool, optional): Whether the value is a regex. Defaults to False.

        Returns:
            bool: Whether the vault contains the metadata.
        """
        if meta_type == MetadataType.FRONTMATTER and key is not None:
            return dict_contains(self.frontmatter, key, value, is_regex)

        if meta_type == MetadataType.INLINE and key is not None:
            return dict_contains(self.inline_meta, key, value, is_regex)

        if meta_type == MetadataType.TAGS and value is not None:
            if not is_regex:
                value = f"^{re.escape(value)}$"
            return any(re.search(value, item) for item in self.tags)

        if meta_type == MetadataType.META:
            return self.contains_metadata(
                MetadataType.FRONTMATTER, key, value, is_regex
            ) or self.contains_metadata(MetadataType.INLINE, key, value, is_regex)

        if meta_type == MetadataType.ALL:
            return self.contains_metadata(
                MetadataType.TAGS, key, value, is_regex
            ) or self.contains_metadata(MetadataType.META, key, value, is_regex)

        return False

    def delete_backup(self) -> None:
        """Delete the vault backup."""
        log.debug("Deleting vault backup")
        if self.backup_path.exists() and self.dry_run is False:
            shutil.rmtree(self.backup_path)
            alerts.success("Backup deleted")
        elif self.backup_path.exists() and self.dry_run is True:
            alerts.dryrun("Delete backup")
        else:
            alerts.info("No backup found")

    def delete_tag(self, tag: str) -> int:
        """Delete an inline tag in the vault.

        Args:
            tag (str): Tag to delete.

        Returns:
            int: Number of notes that had tag deleted.
        """
        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.delete_metadata(MetadataType.TAGS, value=tag):
                log.trace(f"Deleted tag from {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def delete_metadata(
        self,
        key: str,
        value: str | None = None,
        meta_type: MetadataType = MetadataType.ALL,
        is_regex: bool = False,
    ) -> int:
        """Delete metadata in the vault.

        Args:
            meta_type (MetadataType): Area of metadata to delete from.
            is_regex (bool): Whether to use regex for key and value. Defaults to False.
            key (str): Key to delete. Regex is supported
            value (str, optional): Value to delete. Regex is supported

        Returns:
            int: Number of notes that had metadata deleted.
        """
        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.delete_metadata(meta_type=meta_type, key=key, value=value, is_regex=is_regex):
                log.trace(f"Deleted metadata from {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def export_metadata(self, path: str, export_format: str = "csv") -> None:
        """Write metadata to a csv file.

        Args:
            path (Path): Path to write csv file to.
            export_format (str, optional): Export as 'csv' or 'json'. Defaults to "csv".
        """
        export_file = Path(path).expanduser().resolve()
        if not export_file.parent.exists():
            alerts.error(f"Path does not exist: {export_file.parent}")
            raise typer.Exit(code=1)

        match export_format:
            case "csv":
                with export_file.open(mode="w", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Metadata Type", "Key", "Value"])

                    for key, value in self.frontmatter.items():
                        if len(value) > 0:
                            for v in value:
                                writer.writerow(["frontmatter", key, v])
                        else:
                            writer.writerow(["frontmatter", key, ""])

                    for key, value in self.inline_meta.items():
                        if len(value) > 0:
                            for v in value:
                                writer.writerow(["inline_metadata", key, v])
                        else:
                            writer.writerow(["inline_metadata", key, ""])

                    for tag in self.tags:
                        writer.writerow(["tags", "", f"{tag}"])

            case "json":
                dict_to_dump = {
                    "frontmatter": self.frontmatter,
                    "inline_metadata": self.inline_meta,
                    "tags": self.tags,
                }

                with export_file.open(mode="w", encoding="utf-8") as f:
                    json.dump(dict_to_dump, f, indent=4, ensure_ascii=False, sort_keys=True)

    def export_notes_to_csv(self, path: str) -> None:
        """Export notes and their associated metadata to a csv file. This is useful as a template for importing metadata changes to a vault.

        Args:
            path (str): Path to write csv file to.
        """
        export_file = Path(path).expanduser().resolve()
        if not export_file.parent.exists():
            alerts.error(f"Path does not exist: {export_file.parent}")
            raise typer.Exit(code=1)

        with export_file.open(mode="w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["path", "type", "key", "value"])

            for _note in self.all_notes:
                for field in sorted(
                    _note.metadata,
                    key=lambda x: (
                        x.meta_type.name,
                        x.clean_key,
                        x.normalized_value,
                    ),
                ):
                    writer.writerow(
                        [
                            _note.note_path.relative_to(self.vault_path),
                            field.meta_type.name,
                            field.clean_key if field.clean_key is not None else "",
                            field.normalized_value if field.normalized_value != "-" else "",
                        ]
                    )

    def get_changed_notes(self) -> list[Note]:
        """Return a list of notes that have changes.

        Returns:
            list[Note]: List of notes that have changes.
        """
        changed_notes = []
        for _note in self.notes_in_scope:
            if _note.has_changes():
                changed_notes.append(_note)

        return sorted(changed_notes, key=lambda x: x.note_path)

    def info(self) -> None:
        """Print information about the vault."""
        table = Table(show_header=False)
        table.add_row("Vault", str(self.vault_path))
        if self.backup_path.exists():
            table.add_row("Backup path", str(self.backup_path))
        else:
            table.add_row("Backup", "None")
        table.add_row("Notes in scope", str(len(self.notes_in_scope)))
        table.add_row("Notes excluded from scope", str(self.num_excluded_notes()))
        table.add_row("Active filters", str(len(self.filters)))
        table.add_row("Notes with changes", str(len(self.get_changed_notes())))
        table.add_row("Insert Location", str(self.insert_location.value))

        console_no_markup.print(table)

    def list_editable_notes(self) -> None:
        """Print a list of notes within the scope that are being edited."""
        table = Table(title="Notes in current scope", show_header=False, box=box.HORIZONTALS)
        for _n, _note in enumerate(self.notes_in_scope, start=1):
            table.add_row(str(_n), str(_note.note_path.relative_to(self.vault_path)))
        console_no_markup.print(table)

    def move_inline_metadata(self, location: InsertLocation) -> int:
        """Move all inline metadata to the selected location.

        Args:
            location (InsertLocation): Location to move inline metadata to.

        Returns:
            int: Number of notes that had inline metadata moved.
        """
        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.transpose_metadata(
                begin=MetadataType.INLINE,
                end=MetadataType.INLINE,
                key=None,
                value=None,
                location=location,
            ):
                log.trace(f"Moved inline metadata in {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def num_excluded_notes(self) -> int:
        """Count number of excluded notes."""
        return len(self.all_notes) - len(self.notes_in_scope)

    def print_metadata(self, meta_type: MetadataType = MetadataType.ALL) -> None:
        """Print metadata for the vault."""
        dict_to_print = None
        list_to_print = None
        match meta_type:
            case MetadataType.INLINE:
                dict_to_print = self.inline_meta
                header = "All inline metadata"
            case MetadataType.FRONTMATTER:
                dict_to_print = self.frontmatter
                header = "All frontmatter"
            case MetadataType.TAGS:
                list_to_print = [f"#{x}" for x in self.tags]
                header = "All inline tags"
            case MetadataType.KEYS:
                list_to_print = sorted(
                    merge_dictionaries(self.frontmatter, self.inline_meta).keys()
                )
                header = "All Keys"
            case MetadataType.ALL:
                dict_to_print = merge_dictionaries(self.frontmatter, self.inline_meta)
                list_to_print = [f"#{x}" for x in self.tags]
                header = "All metadata"

        if dict_to_print is not None:
            table = Table(title=header, show_footer=False, show_lines=True)
            table.add_column("Keys", style="bold")
            table.add_column("Values")
            for key, value in sorted(dict_to_print.items()):
                values: str | dict[str, list[str]] = (
                    "\n".join(sorted(value)) if isinstance(value, list) else value
                )
                table.add_row(f"{key}", str(values))
            console_no_markup.print(table)

        if list_to_print is not None:
            columns = Columns(
                sorted(list_to_print),
                equal=True,
                expand=True,
                title=header if meta_type != MetadataType.ALL else "All inline tags",
            )
            console_no_markup.print(columns)

    def rename_tag(self, old_tag: str, new_tag: str) -> int:
        """Rename an inline tag in the vault.

        Args:
            old_tag (str): Old tag name.
            new_tag (str): New tag name.

        Returns:
            int: Number of notes that had inline tags renamed.
        """
        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.rename_tag(old_tag, new_tag):
                log.trace(f"Renamed inline tag in {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def rename_metadata(self, key: str, value_1: str, value_2: str | None = None) -> int:
        """Rename a key or key-value pair in the note's metadata.

        If no value is provided, will rename an entire key.

        Args:
            key (str): Key to rename.
            value_1 (str): Value to rename or new name of key if no value_2 is provided.
            value_2 (str, optional): New value.

        Returns:
            int: Number of notes that had metadata renamed.
        """
        num_changed = 0

        for _note in self.notes_in_scope:
            if _note.rename_metadata(key, value_1, value_2):
                log.trace(f"Renamed metadata in {_note.note_path}")
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed

    def transpose_metadata(
        self,
        begin: MetadataType,
        end: MetadataType,
        key: str | None = None,
        value: str | None = None,
        location: InsertLocation = None,
    ) -> int:
        """Transpose metadata from one type to another.

        Args:
            begin (MetadataType): Metadata type to transpose from.
            end (MetadataType): Metadata type to transpose to.
            key (str, optional): Key to transpose. Defaults to None.
            value (str, optional): Value to transpose. Defaults to None.
            location (InsertLocation, optional): Location to insert metadata. (Defaults to `vault.config.insert_location`)

        Returns:
            int: Number of notes that had metadata transposed.
        """
        if location is None:
            location = self.insert_location

        num_changed = 0
        for _note in self.notes_in_scope:
            if _note.transpose_metadata(
                begin=begin,
                end=end,
                key=key,
                value=value,
                location=location,
            ):
                num_changed += 1

        if num_changed > 0:
            self._rebuild_vault_metadata()
            log.trace(f"Transposed metadata in {_note.note_path}")

        return num_changed

    def update_from_dict(self, dictionary: dict[str, Any]) -> int:
        """Update note metadata from a dictionary. This method is used when updating note metadata from a CSV file.  This is a destructive operation. All existing metadata in the specified notes not in the dictionary will be removed.

        Requires a dictionary with the note path as the key and a dictionary of metadata as the value.  Each key must have a list of associated dictionaries in the following format:

            {
                'type': 'frontmatter|inline_metadata|tag',
                'key': 'string',
                'value': 'string'
            }

        Args:
            dictionary (dict[str, Any]): Dictionary to update metadata from.

        Returns:
            int: Number of notes that had metadata updated.
        """
        num_changed = 0

        for _note in self.all_notes:
            path = _note.note_path.relative_to(self.vault_path)
            if str(path) in dictionary:
                log.debug(f"Bulk update metadata for '{path}'")
                num_changed += 1

                # Deleta all existing metadata in the note
                _note.delete_metadata(meta_type=MetadataType.META, key=r".*", is_regex=True)
                _note.delete_metadata(meta_type=MetadataType.TAGS, value=r".*", is_regex=True)

                # Add the new metadata
                for row in dictionary[str(path)]:
                    if row["type"].lower() == "frontmatter":
                        _note.add_metadata(
                            meta_type=MetadataType.FRONTMATTER,
                            added_key=row["key"],
                            added_value=row["value"],
                        )

                    if row["type"].lower() == "inline_metadata":
                        _note.add_metadata(
                            meta_type=MetadataType.INLINE,
                            added_key=row["key"],
                            added_value=row["value"],
                            location=self.insert_location,
                        )

                    if row["type"].lower() == "tag":
                        _note.add_metadata(
                            meta_type=MetadataType.TAGS,
                            added_value=row["value"],
                            location=self.insert_location,
                        )

        if num_changed > 0:
            self._rebuild_vault_metadata()

        return num_changed
