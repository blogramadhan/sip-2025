#!/usr/bin/env python3
"""
Script untuk update dependencies ke versi terbaru
Dengan pengecekan kompatibilitas
"""

import subprocess
import sys
import json

# Mapping dependencies dengan versi minimum yang aman
# Based on testing dan kompatibilitas Streamlit
SAFE_VERSIONS = {
    # Core Streamlit
    "streamlit": "1.40.0",  # Latest stable

    # Data Processing
    "pandas": "2.2.0",
    "numpy": "2.0.0",  # Note: pandas 2.2+ compatible dengan numpy 2.0+
    "pyarrow": "18.1.0",
    "fastparquet": "2024.11.0",

    # Database
    "duckdb": "1.1.0",

    # Visualization
    "plotly": "5.24.0",
    "altair": "5.4.0",

    # Streamlit Components
    "streamlit-aggrid": "1.0.5",
    "streamlit-extras": "0.4.7",

    # Utilities
    "babel": "2.16.0",
    "openpyxl": "3.1.5",
    "pillow": "11.0.0",
    "requests": "2.32.0",
    "click": "8.1.8",
    "rich": "13.9.0",
    "tenacity": "9.0.0",
    "cachetools": "5.5.0",
    "watchdog": "6.0.0",
    "diskcache": "5.6.3",

    # Streamlit Dependencies
    "blinker": "1.9.0",
    "protobuf": "5.29.0",  # Updated from pinned 4.25.3
    "pydeck": "0.9.1",
    "tornado": "6.4.2",
    "toml": "0.10.2",
    "validators": "0.34.0",

    # Time & Date
    "pytz": "2024.2",
    "tzlocal": "5.2",
    "python-dateutil": "2.9.0",

    # Git
    "gitpython": "3.1.43",

    # Utils
    "pympler": "1.1",
    "python-decouple": "3.8",
}

def get_current_versions():
    """Get currently installed versions"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = json.loads(result.stdout)
        return {pkg["name"].lower(): pkg["version"] for pkg in packages}
    except Exception as e:
        print(f"Error getting current versions: {e}")
        return {}

def get_latest_versions(packages):
    """Get latest available versions from PyPI"""
    latest = {}
    for package in packages:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "index", "versions", package],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Parse output untuk mendapatkan latest version
            output = result.stdout
            if "Available versions:" in output:
                versions_line = output.split("Available versions:")[1].split("\n")[0]
                versions_list = [v.strip() for v in versions_line.split(",")]
                if versions_list:
                    latest[package] = versions_list[0]
        except Exception:
            # Jika gagal, gunakan versi dari SAFE_VERSIONS
            if package in SAFE_VERSIONS:
                latest[package] = SAFE_VERSIONS[package]

    return latest

def update_requirements_file():
    """Update requirements.txt dengan versi terbaru yang aman"""

    print("=" * 80)
    print("UPDATING REQUIREMENTS.TXT")
    print("=" * 80)
    print()

    # Baca requirements.txt saat ini
    with open("requirements.txt", "r") as f:
        current_reqs = f.readlines()

    # Parse dan update
    updated_reqs = []

    print("Package updates:")
    print("-" * 80)

    for line in current_reqs:
        line = line.strip()

        # Skip empty lines dan comments
        if not line or line.startswith("#"):
            updated_reqs.append(line)
            continue

        # Parse package name dan operator
        if ">=" in line:
            package_name = line.split(">=")[0].strip()
            operator = ">="
        elif "==" in line:
            package_name = line.split("==")[0].strip()
            operator = "=="
        else:
            updated_reqs.append(line)
            continue

        # Get safe version
        safe_ver = SAFE_VERSIONS.get(package_name.lower())

        if safe_ver:
            new_line = f"{package_name}>={safe_ver}"
            updated_reqs.append(new_line)

            # Extract old version untuk comparison
            old_ver = line.split(operator)[1].strip() if operator in line else "unknown"

            # Simple version comparison (works for most cases)
            try:
                old_parts = [int(x) for x in old_ver.split('.')]
                new_parts = [int(x) for x in safe_ver.split('.')]

                # Pad to same length
                max_len = max(len(old_parts), len(new_parts))
                old_parts += [0] * (max_len - len(old_parts))
                new_parts += [0] * (max_len - len(new_parts))

                if new_parts > old_parts:
                    print(f"✓ {package_name:25s} {old_ver:15s} -> {safe_ver:15s} (UPGRADE)")
                elif new_parts == old_parts:
                    print(f"  {package_name:25s} {old_ver:15s} (no change)")
                else:
                    print(f"⚠ {package_name:25s} {old_ver:15s} -> {safe_ver:15s} (DOWNGRADE - for compatibility)")
            except:
                print(f"  {package_name:25s} {old_ver:15s} -> {safe_ver:15s}")
        else:
            # Keep original if not in SAFE_VERSIONS
            updated_reqs.append(line)
            print(f"  {package_name:25s} (keeping original)")

    print()

    # Write updated requirements
    with open("requirements.txt", "w") as f:
        f.write("\n".join(updated_reqs))
        if updated_reqs and not updated_reqs[-1].endswith("\n"):
            f.write("\n")

    print("✓ requirements.txt updated!")
    print()

def upgrade_venv():
    """Upgrade packages in virtual environment"""

    print("=" * 80)
    print("UPGRADING VIRTUAL ENVIRONMENT")
    print("=" * 80)
    print()

    print("Step 1: Upgrading pip, setuptools, and wheel...")
    print("-" * 80)

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
            check=True
        )
        print("✓ pip, setuptools, and wheel upgraded!")
    except Exception as e:
        print(f"✗ Error upgrading pip tools: {e}")
        return False

    print()
    print("Step 2: Installing updated requirements...")
    print("-" * 80)

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"],
            check=True
        )
        print("✓ All requirements installed/upgraded!")
    except Exception as e:
        print(f"✗ Error installing requirements: {e}")
        return False

    print()
    return True

def verify_installation():
    """Verify critical packages are installed correctly"""

    print("=" * 80)
    print("VERIFYING INSTALLATION")
    print("=" * 80)
    print()

    critical_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "plotly",
        "duckdb",
    ]

    all_ok = True

    for package in critical_packages:
        try:
            __import__(package)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True,
                check=True
            )

            # Extract version
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    ver = line.split(":")[1].strip()
                    print(f"✓ {package:20s} version {ver}")
                    break
        except Exception as e:
            print(f"✗ {package:20s} FAILED: {e}")
            all_ok = False

    print()

    if all_ok:
        print("✓ All critical packages verified!")
    else:
        print("✗ Some packages failed verification!")

    return all_ok

def main():
    """Main execution"""

    print()
    print("=" * 80)
    print("DEPENDENCY UPDATE SCRIPT")
    print("=" * 80)
    print()

    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠ WARNING: You don't appear to be in a virtual environment!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    print()

    # Update requirements.txt
    update_requirements_file()

    # Ask user if they want to upgrade venv
    print("Do you want to upgrade the virtual environment now?")
    response = input("This will install all updated packages (y/n): ")

    if response.lower() == 'y':
        print()
        if upgrade_venv():
            verify_installation()
        else:
            print("✗ Upgrade failed!")
            sys.exit(1)
    else:
        print()
        print("Skipping virtual environment upgrade.")
        print("To upgrade later, run:")
        print("  pip install --upgrade -r requirements.txt")

    print()
    print("=" * 80)
    print("UPDATE COMPLETE!")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
