# Standard libraries
import datetime
from pathlib import Path
from typing import Literal
import re

# Non-standard libraries
import tomlkit
import tomlkit.items

from repodynamics.meta.manager import MetaManager


class PackageFileSync:

    def __init__(self, sync_manager: MetaManager):
        self._manager = sync_manager
        self._logger = self._manager.logger
        self._meta = self._manager.metadata
        self._root = self._manager.path_root
        self._path_pyproject = self._root / "pyproject.toml"
        if not self._path_pyproject.is_file():
            raise ValueError(f"Path {self._path_pyproject} is not a file.")
        with open(self._path_pyproject) as f:
            self._file: tomlkit.TOMLDocument = tomlkit.load(f)
            self._file_raw: str = f.read()
        return

    def update(self):
        self.update_pyproject_toml()
        self.update_package_dir()
        self.update_package_init()
        return

    def update_pyproject_toml(self):
        self.update_project_table()
        self.update_versioningit_onbuild()
        self._manager.update(
            category="package",
            name="pyproject.toml",
            path=self._path_pyproject,
            new_content=tomlkit.dumps(self._file)
        )
        return

    def update_project_table(self):
        data_type = {
            "name": ("str", self._meta["package"]["name"]),
            "description": ("str", self._meta["tagline"]),
            "readme": ("str", ".local/README_PYPI.md"),
            "requires-python": ("str", f">= {self._meta['package']['python_version_min']}"),
            "license": ("inline_table", {"file": "LICENSE"}),
            "authors": ("array_of_inline_tables", self.authors),
            "maintainers": ("array_of_inline_tables", self.maintainers),
            "keywords": ("array", self._meta["keywords"]),
            "classifiers": ("array", self._meta["package"]["trove_classifiers"]),
            "urls": ("table", self.urls),
            "scripts": ("table", self.scripts),
            "gui-scripts": ("table", self.gui_scripts),
            "entry-points": ("table_of_tables", self.entry_points),
            "dependencies": ("array", self.dependencies),
            "optional-dependencies": ("table_of_arrays", self.optional_dependencies),
        }
        for key, (dtype, val) in data_type.items():
            if not val:
                continue
            if dtype == "str":
                toml_val = val
            elif dtype == "array":
                toml_val = tomlkit.array(val).multiline(True)
            elif dtype == "table":
                toml_val = val
            elif dtype == "inline_table":
                toml_val = tomlkit.inline_table()
                toml_val.update(val)
            elif dtype == "array_of_inline_tables":
                toml_val = tomlkit.array().multiline(True)
                for table in val:
                    tab = tomlkit.inline_table()
                    tab.update(table)
                    toml_val.append(tab)
            elif dtype == "table_of_arrays":
                toml_val = {
                    tab_key: tomlkit.array(arr).multiline(True) for tab_key, arr in val.items()
                }
            elif dtype == "table_of_tables":
                toml_val = tomlkit.table(is_super_table=True).update(val)
            else:
                raise ValueError(f"Unknown data type {dtype} for key {key}.")
            self._file["project"][key] = toml_val
        return

    def _get_authors_maintainers(self, role: Literal["authors", "maintainers"]):
        """
        Update the project authors in the pyproject.toml file.

        References
        ----------
        https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#authors-maintainers
        """
        people = []
        for person in self._meta[role]:
            if not person["name"]:
                self._logger.warning(
                    f'One of {role} with username \'{person["username"]}\' '
                    f'has no name set in their GitHub account. They will be dropped from the list of {role}.'
                )
                continue
            user = {"name": person["name"]}
            email = person.get("email")
            if email:
                user["email"] = email
            people.append(user)
        return people

    @property
    def urls(self):
        # For list of URL keys, see:
        # https://github.com/pypi/warehouse/blob/e69029dc1b23eb2436a940038b927e772238a7bf/warehouse/templates/packaging/detail.html#L20-L62
        return {
            "Homepage": self._meta['url']['website']['base'],
            "Download": self._meta['url']['github']['releases']['home'],
            "News": self._meta['url']['website']['news'],
            "Documentation": self._meta['url']['website']['base'],
            "Bug Tracker": self._meta['url']['github']['issues']['home'],
            "Sponsor": self._meta['url']['website']['sponsor'],
            "Source": self._meta['url']['github']['home'],
        }

    @property
    def authors(self):
        return self._get_authors_maintainers(role="authors")

    @property
    def maintainers(self):
        return self._get_authors_maintainers(role="maintainers")

    @property
    def dependencies(self):
        if not self._meta["package"].get("dependencies"):
            return
        return [dep["pip_spec"] for dep in self._meta["package"]["dependencies"]]

    @property
    def optional_dependencies(self):
        return {
            dep_group["name"]: [dep["pip_spec"] for dep in dep_group["packages"]]
            for dep_group in self._meta["package"]["optional_dependencies"]
        } if self._meta["package"].get("optional_dependencies") else None

    @property
    def scripts(self):
        return self._scripts(gui=False)

    @property
    def gui_scripts(self):
        return self._scripts(gui=True)

    def _scripts(self, gui: bool):
        cat = "gui_scripts" if gui else "scripts"
        return {
            script["name"]: script["ref"]
            for script in self._meta["package"][cat]
        } if self._meta["package"].get(cat) else None

    @property
    def entry_points(self):
        return {
            entry_group["group_name"]: {
                entry_point["name"]: entry_point["ref"]
                for entry_point in entry_group["entry_points"]
            }
            for entry_group in self._meta["package"]["entry_points"]
        } if self._meta["package"].get("entry_points") else None

    def update_versioningit_onbuild(self):
        tab = self._file["tool"]["versioningit"]["onbuild"]
        from_src = f"{self._meta['package']['name']}/__init__.py"
        tab["build-file"] = from_src
        tab["source-file"] = f"src/{from_src}"
        return

    def update_package_dir(self):
        self._logger.section("Update path: package")
        path_src = self._root / "src"
        path_package = path_src / self._meta["package"]["name"]
        if not path_package.exists():
            self._logger.debug(f"Package path '{path_package}' does not exist; looking for package directory.")
            package_dirs = [
                subdir for subdir in [content for content in path_src.iterdir() if content.is_dir()]
                if "__init__.py" in [
                    sub_content.name for sub_content in subdir.iterdir() if sub_content.is_file()
                ]
            ]
            count_dirs = len(package_dirs)
            if count_dirs == 0:
                # self._logger.success(f"No package directory found in '{path_src}'; creating one.")
                # path_package.mkdir()
                self._logger.error(f"No package directory found in '{path_src}'.")
            elif count_dirs == 1:
                self._logger.success(
                    f"Package directory found at '{package_dirs[0]}'; "
                    f"renaming it to '{self._meta['package']['name']}'."
                )
                package_dirs[0].rename(path_package)
                old_path = package_dirs[0].relative_to(self._root)
                self._manager.add_result(
                    category="package",
                    name=f"package directory",
                    result={
                        "status": "moved",
                        "path_before": str(old_path),
                        "path": f"src/{self._meta['package']['name']}"
                    }
                )
                return
            else:
                self._logger.error(f"More than one package directory found in '{path_src}'.")
        else:
            self._logger.success(f"Package path '{path_package}' exists.")
            self._manager.add_result(
                category="package",
                name=f"package directory",
                result={
                    "status": "unchanged",
                    "path": f"src/{self._meta['package']['name']}",
                    "before": "",
                    "after": ""
                }
            )
        return

    def update_package_init(self):
        docstring = f"{self._meta['name']}\n\n{self._meta['tagline']}\n\n{self._meta['description']}"
        if self._meta.get("license_id"):
            filename = self._meta["license_id"].lower().rstrip("+")
            copyright_notice = self._manager.template("license", f"{filename}_notice")
            docstring += f"\n\n{copyright_notice}"
        path_init = self._root / "src" / self._meta["package"]["name"] / "__init__.py"
        with open(path_init) as f:
            text = f.read()
        docstring_pattern = r"(\"\"\")(.*?)(\"\"\")"
        match = re.search(docstring_pattern, text, re.DOTALL)
        if match:
            # Replace the existing docstring with the new one
            new_text = re.sub(docstring_pattern, rf"\1{docstring}\3", text, flags=re.DOTALL)
        else:
            # If no docstring found, add the new docstring at the beginning of the file
            new_text = f'"""\n{docstring}\n"""\n{text}'
        # Write the modified content back to the file
        self._manager.update(category="package", name="__init__.py", path=path_init, new_content=new_text)
        return

    def update_header_comment(self):
        lines = [
            f"{self._meta['project']['name']} pyproject.toml File.",
            (
                "Automatically generated on "
                f"{datetime.datetime.utcnow().strftime('%Y.%m.%d at %H:%M:%S UTC')} "
                f"by PyPackIT"
            ),
            "This file contains build system requirements and information,",
            " which are used by pip to build the package.",
            " For more information, see https://pypackit.readthedocs.io",
        ]
        for line_idx, line in enumerate(lines):
            self._file.body[line_idx][1].trivia.comment = f"# {line}"
        return

