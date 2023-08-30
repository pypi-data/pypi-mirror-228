

import os
import tarfile
from typing import Optional
from janis_core.settings.ingest.galaxy import DOWNLOADED_WRAPPERS_DIR
from janis_core.ingestion.galaxy.fileio import safe_init_folder


class DownloadCache:
    """
    keeps track of the location of downloaded wrapper folders.
    DownloadCache.get() will return the local path to a tool xml if already downloaded
    DownloadCache.add() saves a tar as a download and notes its path. 
    """

    def get(self, query_repo: str, query_revision: str) -> Optional[str]:
        """returns the local file path for the tool xml if already downloaded or None"""
        path = DOWNLOADED_WRAPPERS_DIR
        for folder in self._load():
            repo, revision = folder.split('-', 1)
            if repo == query_repo and revision == query_revision:
                return f'{path}{os.sep}{folder}'
        return None

    def add(self, tar: tarfile.TarFile) -> None:
        self._save(tar)

    def _save(self, tar: tarfile.TarFile) -> None:
        path = DOWNLOADED_WRAPPERS_DIR
        safe_init_folder(path)
        tar.extractall(path=path)

    def _load(self) -> set[str]:
        path = DOWNLOADED_WRAPPERS_DIR
        safe_init_folder(path)
        folders = os.listdir(path)
        folders = [f for f in folders if os.path.isdir(f'{path}{os.sep}{f}')]
        return set(folders)

