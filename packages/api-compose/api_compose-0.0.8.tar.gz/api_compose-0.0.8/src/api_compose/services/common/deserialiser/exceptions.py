import json
from pathlib import Path
from typing import Dict, List

from api_compose.core.utils.list import get_duplicates_in_list
from api_compose.services.common.deserialiser.checks import get_file_names_in, get_file_paths_relative_to


# Manifest Folder Exception
class EmptyManifestFolderException(Exception):
    def __init__(self,
                 manifest_folder_path: Path,
                 ):
        self.manifest_folder_path = manifest_folder_path

    def __str__(self):
        return (f"No manifests are found in the folder {self.manifest_folder_path}. \m"
                f"Are you in the right directory?")


# Manifest Content Exception
class ManifestMissingModelNameException(Exception):
    def __init__(self,
                 manifest_file_path: str,
                 manifest_content: Dict,
                 available_model_names: List[str],
                 ):
        self.manifest_file_path = manifest_file_path
        self.manifest_content = manifest_content
        self.available_model_names = available_model_names

    def __str__(self):
        return (f"Missing Key ***model_name*** in manifest {self.manifest_file_path=} with content \n"
                f"{json.dumps(self.manifest_content, indent=4)} \n"
                f"Please add a key-value pair with key **model_name**. {self.available_model_names=}")


# Manifest File Name Exception
class NonUniqueManifestNameException(Exception):
    def __init__(self,
                 manifest_folder_path: Path,
                 ):
        self.manifest_folder_path = manifest_folder_path

        self.file_paths_with_identifical_file_names = {
            f: get_file_paths_relative_to(manifest_folder_path, f) for f in get_duplicates_in_list(
                get_file_names_in(manifest_folder_path)
            )
        }

    def __str__(self):
        return (f"Path {self.manifest_folder_path} has the below file paths with identical file names \n"
                f"{self.file_paths_with_identifical_file_names}. \n"
                f"Please eliminate identical files \n"
                )


class ManifestNotFoundException(Exception):
    def __init__(self,
                 manifest_folder_path: Path,
                 manifest_file_name: str,
                 ):
        self.manifest_folder_path = manifest_folder_path
        self.manifest_file_name = manifest_file_name

    def __str__(self):
        return f"No manifest {self.manifest_file_name} is found in Path {self.manifest_folder_path}"
