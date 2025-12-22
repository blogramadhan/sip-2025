#!/usr/bin/env python3
"""
Debug script untuk investigasi masalah di Docker production
Jalankan script ini di dalam container untuk diagnosis
"""
import os
import sys

def debug_environment():
    """Print informasi environment untuk debugging"""

    print("=" * 80)
    print("DOCKER ENVIRONMENT DEBUG INFO")
    print("=" * 80)
    print()

    # 1. Python info
    print("1. PYTHON INFORMATION")
    print("-" * 80)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()

    # 2. Working directory
    print("2. WORKING DIRECTORY")
    print("-" * 80)
    print(f"Current working directory: {os.getcwd()}")
    print()

    # 3. Directory listing
    print("3. DIRECTORY CONTENTS")
    print("-" * 80)
    try:
        files = os.listdir(os.getcwd())
        print(f"Files in {os.getcwd()}:")
        for f in sorted(files):
            path = os.path.join(os.getcwd(), f)
            if os.path.isdir(path):
                print(f"  [DIR]  {f}/")
            else:
                size = os.path.getsize(path)
                print(f"  [FILE] {f} ({size:,} bytes)")
    except Exception as e:
        print(f"Error listing directory: {e}")
    print()

    # 4. Public directory check
    print("4. PUBLIC DIRECTORY CHECK")
    print("-" * 80)
    public_dir = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_dir):
        print(f"✓ Public directory exists: {public_dir}")
        print(f"  Permissions: {oct(os.stat(public_dir).st_mode)[-3:]}")
        print()
        try:
            files = os.listdir(public_dir)
            print(f"  Files in public/:")
            for f in sorted(files):
                path = os.path.join(public_dir, f)
                size = os.path.getsize(path)
                perms = oct(os.stat(path).st_mode)[-3:]
                print(f"    - {f} ({size:,} bytes, perms: {perms})")
        except Exception as e:
            print(f"  Error listing public directory: {e}")
    else:
        print(f"✗ Public directory NOT found: {public_dir}")
    print()

    # 5. Logo files check
    print("5. LOGO FILES CHECK")
    print("-" * 80)
    logo_files = [
        "public/sip-spse.png",
        "public/sip-spse-icon.png",
        "public/OPSI-1.png"
    ]
    for logo_file in logo_files:
        full_path = os.path.join(os.getcwd(), logo_file)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            perms = oct(os.stat(full_path).st_mode)[-3:]
            print(f"✓ {logo_file}")
            print(f"  Path: {full_path}")
            print(f"  Size: {size:,} bytes")
            print(f"  Permissions: {perms}")

            # Try to read
            try:
                with open(full_path, 'rb') as f:
                    f.read(10)
                print(f"  Readable: YES")
            except Exception as e:
                print(f"  Readable: NO - {e}")
        else:
            print(f"✗ {logo_file} NOT FOUND")
            print(f"  Expected path: {full_path}")
        print()

    # 6. Environment variables
    print("6. RELEVANT ENVIRONMENT VARIABLES")
    print("-" * 80)
    env_vars = ['HOME', 'USER', 'PATH', 'PYTHONPATH', 'STREAMLIT_SERVER_HEADLESS']
    for var in env_vars:
        value = os.environ.get(var, '<not set>')
        print(f"  {var}: {value}")
    print()

    # 7. User and permissions
    print("7. USER AND PERMISSIONS")
    print("-" * 80)
    try:
        import pwd
        uid = os.getuid()
        user_info = pwd.getpwuid(uid)
        print(f"  Current UID: {uid}")
        print(f"  Current user: {user_info.pw_name}")
        print(f"  Home directory: {user_info.pw_dir}")
    except Exception as e:
        print(f"  Could not get user info: {e}")
    print()

    print("=" * 80)
    print("END OF DEBUG INFO")
    print("=" * 80)

if __name__ == "__main__":
    debug_environment()
