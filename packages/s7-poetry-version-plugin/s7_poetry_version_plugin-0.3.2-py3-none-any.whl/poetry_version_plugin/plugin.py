import ast
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from cleo.io.io import IO
# from poetry.core.utils.helpers import module_name
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry


class VersionPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO) -> None:
        poetry_version_config: Optional[Dict[str, Any]] = poetry.pyproject.data.get(
            "tool", {}
        ).get("poetry-version-plugin")
        if poetry_version_config is None:
            return
        version_source = poetry_version_config.get("source")
        if not version_source:
            message = (
                "<b>poetry-version-plugin</b>: No <b>source</b> configuration found in "
                "[tool.poetry-version-plugin] in pyproject.toml, not extracting "
                "dynamic version"
            )
            io.write_error_line(message)
            raise RuntimeError(message)
        if version_source == "init":
            set_from_init(poetry, io)
        elif version_source == "version":
            set_from_version(poetry, io)
        elif version_source == "git-tag":
            set_from_git(poetry, io)


def set_from_init(poetry: Poetry, io: IO):
    packages = poetry.local_config.get("packages")
    if packages:
        if len(packages) >= 1:
            package_name = packages[0]["include"]
        else:
            message = (
                "<b>poetry-version-plugin</b>: Not package set, "
                "cannot extract dynamic version"
            )
            io.write_error_line(message)
            raise RuntimeError(message)
    else:
        # package_name = module_name(poetry.package.name)
        package_name = "."
    init_path = Path(package_name) / "__init__.py"
    if not init_path.is_file():
        message = (
            "<b>poetry-version-plugin</b>: __init__.py file not found at "
            f"{init_path} cannot extract dynamic version"
        )
        io.write_error_line(message)
        raise RuntimeError(message)
    io.write_line(
        "<b>poetry-version-plugin</b>: Using __init__.py file at "
        f"{init_path} for dynamic version"
    )
    if version := extract_from_init(init_path):
        io.write_line(
            "<b>poetry-version-plugin</b>: Setting package "
            "dynamic version to __version__ "
            f"variable from __init__.py: <b>{version}</b>"
        )
        poetry.package._set_version(version)
        return
    message = (
        "<b>poetry-version-plugin</b>: No valid __version__ variable found "
        "in __init__.py, cannot extract dynamic version"
    )
    io.write_error_line(message)
    raise RuntimeError(message)


def set_from_version(poetry: Poetry, io: IO):
    init_path = Path(".") / "version.py"
    if not init_path.is_file():
        message = (
            "<b>poetry-version-plugin</b>: version.py file not found at "
            f"{init_path} cannot extract dynamic version"
        )
        io.write_error_line(message)
        raise RuntimeError(message)
    io.write_line(
        "<b>poetry-version-plugin</b>: Using version.py file at "
        f"{init_path} for dynamic version"
    )
    if version := extract_from_version(init_path):
        io.write_line(
            "<b>poetry-version-plugin</b>: Setting package "
            "dynamic version to __version__ "
            f"variable from version.py: <b>{version}</b>"
        )
        poetry.package._set_version(version)
        return
    message = (
        "<b>poetry-version-plugin</b>: No valid variable found "
        "in version.py, cannot extract dynamic version"
    )
    io.write_error_line(message)
    raise RuntimeError(message)


def extract_from_init(init_path):
    tree = ast.parse(init_path.read_text())
    for el in tree.body:
        if not isinstance(el, ast.Assign):
            continue
        if len(el.targets) != 1:
            continue
        target = el.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id != "__version__":
            continue
        value_node = el.value
        if isinstance(value_node, ast.Constant):
            return value_node.value
        elif isinstance(value_node, ast.Str):
            return value_node.s
        # pragma: nocover
        # This is actually covered by tests, but can't be
        # reported by Coverage
        # Ref: https://github.com/nedbat/coveragepy/issues/198


def extract_from_version(init_path):
    keys = ('major', 'minor', 'patch', 'micro')
    value = dict.fromkeys(keys, 0)
    tree = ast.parse(init_path.read_text())
    for el in tree.body:
        if not isinstance(el, ast.Assign):
            continue
        if not len(el.targets) == 1:
            continue
        target = el.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if target.id not in keys:
            continue
        value_node = el.value
        if isinstance(value_node, ast.Constant):
            value[target.id] = value_node.value
        # elif isinstance(value_node, ast.Str):
        #     value[target.id] = value_node.s
        # pragma: nocover
        # This is actually covered by tests, but can't be
        # reported by Coverage
        # Ref: https://github.com/nedbat/coveragepy/issues/198
    return f"{value['major']}.{value['minor']}.{value['patch']}.{value['micro']}"


def set_from_git(poetry: Poetry, io: IO):
    result = subprocess.run(
        ["git", "describe", "--exact-match", "--tags", "HEAD"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    if result.returncode == 0:
        tag = result.stdout.strip()
        io.write_line(
            "<b>poetry-version-plugin</b>: Git tag found, setting "
            f"dynamic version to: {tag}"
        )
        poetry.package._set_version(tag)
        return
    else:
        message = (
            "<b>poetry-version-plugin</b>: No Git tag found, not "
            "extracting dynamic version"
        )
        io.write_error_line(message)
        raise RuntimeError(message)
