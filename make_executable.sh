#!/usr/bin/env bash
set -euo pipefail

# Check args
[[ $# -eq 1 && -f "$1" && "${1##*.}" == "py" ]] || { echo "Usage: $0 file.py"; exit 1; }

TARGET="$(realpath "$1")"
DIR="$(dirname "$TARGET")" 
NAME="$(basename "$TARGET" .py)"

# Install/find pyinstaller
PYINSTALLER=""
for cmd in pyinstaller "$HOME/.local/bin/pyinstaller"; do
    if [[ -x "$cmd" ]]; then
        PYINSTALLER="$cmd"
        break
    fi
done

if [[ -z "$PYINSTALLER" ]]; then
    echo "Installing pyinstaller..."
    python3 -m pip install --user pyinstaller
    PYINSTALLER="$HOME/.local/bin/pyinstaller"
    [[ -x "$PYINSTALLER" ]] || PYINSTALLER="$(command -v pyinstaller)"
fi

[[ -x "$PYINSTALLER" ]] || { echo "PyInstaller installation failed"; exit 1; }

# Check Python file
python3 -m py_compile "$TARGET" || { echo "Python syntax errors"; exit 1; }

# Build
echo "Building $NAME..."
"$PYINSTALLER" --onefile \
    --distpath "$DIR" \
    --workpath "/tmp/build_$$" \
    --specpath "/tmp/build_$$" \
    --hidden-import pkg_resources \
    "$TARGET"

# Cleanup
rm -rf "$DIR/build" "$DIR/__pycache__" "/tmp/build_$$"
chmod +x "$DIR/$NAME"

echo "Done: $DIR/$NAME"
