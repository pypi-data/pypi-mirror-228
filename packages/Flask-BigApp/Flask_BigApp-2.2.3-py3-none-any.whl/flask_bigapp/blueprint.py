import logging
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from typing import Optional, Union, Protocol

from flask import Blueprint
from flask import session

from .helpers import init_bp_config
from .utilities import cast_to_import_str, deprecated


class BigApp(Protocol):
    def import_models(
            self,
            from_file: Optional[Union[str, Path]] = None,
            from_folder: Optional[Union[str, Path]] = None,
    ) -> None:
        ...


class BigAppBlueprint(Blueprint):
    """
    Class that handles Blueprints from within the Blueprint __init__ from_file
    """
    enabled: bool = False
    location: Path
    bp_name: str
    package: str
    session: dict
    settings: dict

    _bigapp_instance: BigApp

    def __init__(self, dunder_name, config_file: str = "config.toml"):
        """
        dunder_name must be __name__
        config_file must be relative to the location of the blueprint.
        """
        self.package = dunder_name
        self.app_name = dunder_name.split(".")[0]

        spec = find_spec(self.package)

        if spec is None:
            raise ImportError(f"Cannot find origin of {self.package}")

        self.location = Path(f"{spec.origin}").parent
        self.bp_name = self.location.name

        self.enabled, self.session, self.settings = init_bp_config(self.bp_name, self.location / config_file)

        if self.enabled:
            super().__init__(
                self.bp_name,
                self.package,
                **self.settings
            )
            self._bigapp_instance = self.set_bigapp_instance()

    def set_bigapp_instance(self):
        def get_bigapp_instance() -> BigApp:
            from flask_bigapp import BigApp

            app_module = import_module(self.app_name)
            for dir_item in dir(app_module):
                potential_instance = getattr(app_module, dir_item)
                if isinstance(potential_instance, BigApp):
                    return potential_instance
            raise ImportError(f"Cannot find BigApp instance in {self.app_name}")

        return get_bigapp_instance()

    def import_resources(self, folder: str = "routes") -> None:
        """
        Imports all the resources in the given from_folder.
        If no from_folder is specified defaults to a from_folder named 'routes'

        Folder must be relative
        ( from_folder="here" not from_folder="/home/user/app/from_folder/blueprint/from_folder" )
        """
        if not self.enabled:
            return

        resource_path = self.location / folder
        if not resource_path.exists():
            raise NotADirectoryError(f"{resource_path} is not a directory")

        resources = resource_path.glob("*.py")
        for resource in resources:
            try:
                import_module(f"{self.package}.{folder}.{resource.stem}")
            except ImportError as e:
                logging.warning(f"Error when importing {self.package}.{resource}: {e}")
                continue

    def import_nested_blueprints(self, folder: str) -> None:
        """
        Imports all the blueprints in the given from_folder.

        Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        if not self.enabled:
            return

        folder_path = Path(self.location / folder)

        for potential_bp in folder_path.iterdir():
            self.import_nested_blueprint(potential_bp)

    def import_nested_blueprint(self, blueprint: Union[str, Path]):
        """
        Imports a single blueprint from the given path.

        Path must be relative ( path="here" not path="/home/user/app/from_folder" )
        """
        if not self.enabled:
            return

        if isinstance(blueprint, str):
            potential_bp = Path(self.location / blueprint)
        else:
            potential_bp = blueprint

        if potential_bp.is_dir():
            app_name = self.package.split(".")[0]
            try:
                module = import_module(cast_to_import_str(app_name, potential_bp))
                for dir_item in dir(module):
                    _ = getattr(module, dir_item)
                    if isinstance(_, BigAppBlueprint):
                        if _.enabled:
                            self.register_blueprint(_)
                        break
            except Exception as e:
                logging.critical(f"{e}\n", f"Error importing blueprint: from {potential_bp}")

    def init_session(self) -> None:
        """
        Initialize the session variables found in the config from_file.
        Use this method in the before_request route.
        """
        if not self.enabled:
            return

        for key in self.session:
            if key not in session:
                session.update(self.session)
                break

    def import_models(
            self,
            from_file: Optional[Union[str, Path]] = None,
            from_folder: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Imports model files from a single from_file or a from_folder. Both are allowed to be set.

        File and Folder must be relative ( from_folder="here" not from_folder="/home/user/app/from_folder" )
        """
        if not self.enabled:
            return

        if isinstance(from_file, str):
            from_file = Path(self.location / from_file)

        if isinstance(from_folder, str):
            from_folder = Path(self.location / from_folder)

        self._bigapp_instance.import_models(from_file, from_folder)

    def tmpl(self, template) -> str:
        """
        Pushes together the name of the blueprint and the template from_file to look for.
        This is a small-time saving method to allow you to only type
        bp.tmpl("index.html") when looking for template files.
        """
        return f"{self.name}/{template}"

    @deprecated("import_blueprint_models() is deprecated Use import_models instead")
    def import_blueprint_models(
            self,
            from_file: Optional[str] = None,
            from_folder: Optional[str] = None
    ) -> None:
        self.import_models(from_file=from_file, from_folder=from_folder)
