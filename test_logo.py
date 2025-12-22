#!/usr/bin/env python3
"""
Test script untuk memverifikasi logo path di Docker environment
"""
import os
import sys

def test_logo_paths():
    """Test apakah logo files dapat diakses"""

    # Get base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "public", "sip-spse.png")
    icon_path = os.path.join(base_dir, "public", "sip-spse-icon.png")

    print(f"Base directory: {base_dir}")
    print(f"Logo path: {logo_path}")
    print(f"Icon path: {icon_path}")
    print()

    # Check if files exist
    if os.path.exists(logo_path):
        print(f"✓ Logo file exists: {logo_path}")
        print(f"  Size: {os.path.getsize(logo_path)} bytes")
        print(f"  Permissions: {oct(os.stat(logo_path).st_mode)[-3:]}")
    else:
        print(f"✗ Logo file NOT found: {logo_path}")
        return False

    if os.path.exists(icon_path):
        print(f"✓ Icon file exists: {icon_path}")
        print(f"  Size: {os.path.getsize(icon_path)} bytes")
        print(f"  Permissions: {oct(os.stat(icon_path).st_mode)[-3:]}")
    else:
        print(f"✗ Icon file NOT found: {icon_path}")
        return False

    print()

    # Check if files are readable
    try:
        with open(logo_path, 'rb') as f:
            f.read(10)
        print(f"✓ Logo file is readable")
    except Exception as e:
        print(f"✗ Logo file is NOT readable: {e}")
        return False

    try:
        with open(icon_path, 'rb') as f:
            f.read(10)
        print(f"✓ Icon file is readable")
    except Exception as e:
        print(f"✗ Icon file is NOT readable: {e}")
        return False

    print()
    print("✓ All logo files are accessible and readable!")
    return True

if __name__ == "__main__":
    success = test_logo_paths()
    sys.exit(0 if success else 1)
