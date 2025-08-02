import os
import subprocess
import shutil
import time
from pathlib import Path
from typing import Dict

# Define log directory in user's home directory
log_dir = Path.home() / "package-logs"

# Create timestamp in format YYYYMMDD_HHMMSS
timestamp = time.strftime("%Y%m%d_%H%M%S")

# Ensure log directory exists
log_dir.mkdir(exist_ok=True)


def log_packages(manager: str, cmd: str) -> None:
    """
    Log installed packages for a given package manager to a file.

    Args:
        manager: Name of the package manager
        cmd: Command to list installed packages
    """
    log_file = log_dir / f"{manager}-{timestamp}.txt"
    print(f"📦 Logging {manager} packages...")

    # Split command into executable and arguments
    args = cmd.split()
    executable = args[0]

    # Check if executable exists
    if shutil.which(executable):
        try:
            # Run command and capture output
            output = subprocess.check_output(args, stderr=subprocess.STDOUT, text=True)
            log_file.write_text(output)
            print(f"✅ Saved to {log_file}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Error running {manager}: {e}")
    else:
        print(f"⚠️  {manager} not found, skipping.")


# Define package managers and their commands
pkg_managers: Dict[str, str] = {
    "apt": "apt list --installed",
    "brew": "brew list --versions",
    "snap": "snap list",
    "flatpak": "flatpak list --app --columns=application,version",
    "nix": "nix profile list",
    "cargo": "cargo install --list",
}

# Log packages for each manager
for manager, cmd in pkg_managers.items():
    log_packages(manager, cmd)

print(f"\n📁 All logs saved in: {log_dir}")
