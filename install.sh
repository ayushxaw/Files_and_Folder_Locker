#!/bin/bash
# Installer for Files and Folder Locker for Ubuntu.

set -euo pipefail

REPO_DIR="$(dirname "$(readlink -f "$0")")"
BIN_DIR="$HOME/.local/bin"
EXT_DIR="$HOME/.local/share/nautilus-python/extensions"

echo "Installing dependencies..."
sudo apt update
sudo apt install -y gocryptfs zenity gnupg python3-nautilus

mkdir -p "$BIN_DIR" "$EXT_DIR"

chmod +x "$REPO_DIR/locker-auth" \
         "$REPO_DIR/folder-encrypt" \
         "$REPO_DIR/folder-unlock" \
         "$REPO_DIR/folder-lock" \
         "$REPO_DIR/folder-toggle"

ln -sf "$REPO_DIR/folder-encrypt" "$BIN_DIR/folder-encrypt"
ln -sf "$REPO_DIR/folder-unlock"  "$BIN_DIR/folder-unlock"
ln -sf "$REPO_DIR/folder-lock"    "$BIN_DIR/folder-lock"
ln -sf "$REPO_DIR/folder-toggle"  "$BIN_DIR/folder-toggle"
ln -sf "$REPO_DIR/nautilus-extension/folder_locker.py" "$EXT_DIR/folder_locker.py"

echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true

echo "Done! Right-click any file or folder in Files to encrypt, lock, or unlock it."
