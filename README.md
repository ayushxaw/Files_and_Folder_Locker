# Files and Folder Locker for Ubuntu

A lightweight way to password-protect any folder or file on Ubuntu right from the Files (Nautilus) right-click menu, using your Linux login password as the single master password.

## How it works

- **Folders** are encrypted with `gocryptfs` into a hidden `.<name>_vault` directory next to the folder. When you unlock a folder, it mounts cleanly and opens in Files — and once you close Files, a background watcher automatically locks it again.
- **Files** (PDFs, images, documents, etc.) are encrypted with `gpg` (AES-256) into a `.locked` file, and the original is removed until you unlock it.
- **One password for everything:** instead of managing separate passwords per folder, it checks your Ubuntu user password via `sudo` and uses that for encryption and decryption.

## Installation

```bash
git clone https://github.com/ayushxaw/files-and-folder-locker-for-ubuntu.git
cd files-and-folder-locker-for-ubuntu
./install.sh
```

The installer sets up `gocryptfs`, `zenity`, `gnupg`, and `python3-nautilus`, symlinks the commands into `~/.local/bin`, installs the Nautilus right-click extension, and restarts Files.

## Usage

Open **Files (Nautilus)** and right-click any file or folder in your home directory:

- **Encrypt This Folder / File** — first-time setup; prompts for your password and locks it.
- **Unlock This Folder / File** — prompts for your password and opens/restores it.
- **Lock This Folder** — locks an unlocked folder immediately (or just close Files to auto-lock).

You can also run them from the terminal:

```bash
folder-encrypt /path/to/item
folder-unlock /path/to/item
folder-lock /path/to/folder
```

## Notes

- Don't delete hidden `.<name>_vault` folders — that's where your encrypted folder data lives.
- If you change your Ubuntu login password later, update existing `gocryptfs` vaults to match:
  ```bash
  gocryptfs -passwd ~/Documents/.PERSONAL_vault
  ```
