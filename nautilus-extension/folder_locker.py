"""
Nautilus context menu extension for Files & Folder Locker.
Adds Encrypt, Unlock, and Lock actions to right-click menus for folders and files.
"""

import os
import subprocess
from gi.repository import Nautilus, GObject


HOME = os.path.expanduser("~")
BIN = os.path.join(HOME, ".local", "bin")
ENCRYPT_CMD = os.path.join(BIN, "folder-encrypt")
UNLOCK_CMD = os.path.join(BIN, "folder-unlock")
LOCK_CMD = os.path.join(BIN, "folder-lock")


def _vault_for(path):
    parent = os.path.dirname(path)
    name = os.path.basename(path)
    return os.path.join(parent, f".{name}_vault")


def _has_vault(path):
    return os.path.isfile(os.path.join(_vault_for(path), "gocryptfs.conf"))


def _is_mounted(path):
    try:
        res = subprocess.run(["findmnt", "-M", path], capture_output=True, timeout=3)
        return res.returncode == 0
    except Exception:
        return False


def _run(cmd, path):
    subprocess.Popen(
        [cmd, path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


class FolderLockerExtension(GObject.GObject, Nautilus.MenuProvider):

    def get_file_items(self, *args):
        files = args[-1] if isinstance(args[-1], list) else list(args)
        items = []
        for f in files:
            loc = f.get_location()
            if loc is None:
                continue
            path = loc.get_path()
            if path is None:
                continue

            if f.is_directory():
                items.extend(self._folder_items(path))
            else:
                items.extend(self._file_items(path))
        return items

    def get_background_items(self, *args):
        folder = args[-1] if not isinstance(args[-1], list) else args[-1][0]
        loc = folder.get_location()
        if loc is None:
            return []
        path = loc.get_path()
        if path is None:
            return []
        return self._folder_items(path)

    def _folder_items(self, path):
        items = []
        if _has_vault(path):
            if _is_mounted(path):
                item = Nautilus.MenuItem(
                    name="FolderLocker::Lock",
                    label="Lock This Folder",
                    tip="Lock and encrypt this folder",
                )
                item.connect("activate", self._on_lock, path)
                items.append(item)
            else:
                item = Nautilus.MenuItem(
                    name="FolderLocker::Unlock",
                    label="Unlock This Folder",
                    tip="Enter password to unlock",
                )
                item.connect("activate", self._on_unlock, path)
                items.append(item)
        elif path.startswith(HOME) and path != HOME:
            item = Nautilus.MenuItem(
                name="FolderLocker::Encrypt",
                label="Encrypt This Folder",
                tip="Password-protect this folder",
            )
                
            item.connect("activate", self._on_encrypt, path)
            items.append(item)
        return items

    def _file_items(self, path):
        items = []
        name = os.path.basename(path)

        if name.endswith(".locked"):
            item = Nautilus.MenuItem(
                name="FolderLocker::UnlockFile",
                label="Unlock This File",
                tip="Decrypt this file with your password",
            )
            item.connect("activate", self._on_unlock, path)
            items.append(item)
        elif path.startswith(HOME) and not name.startswith("."):
            item = Nautilus.MenuItem(
                name="FolderLocker::EncryptFile",
                label="Encrypt This File",
                tip="Lock this file with your password",
            )
            item.connect("activate", self._on_encrypt, path)
            items.append(item)
        return items

    def _on_lock(self, menu, path):
        _run(LOCK_CMD, path)

    def _on_unlock(self, menu, path):
        _run(UNLOCK_CMD, path)

    def _on_encrypt(self, menu, path):
        _run(ENCRYPT_CMD, path)
