#!/bin/bash
# Script untuk upgrade virtual environment
# Usage: ./upgrade_venv.sh

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "VIRTUAL ENVIRONMENT UPGRADE SCRIPT"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}✗${NC} Virtual environment not found!"
    echo ""
    echo "Creating new virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✓${NC} Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Failed to activate virtual environment!"
    exit 1
fi

echo -e "${GREEN}✓${NC} Virtual environment activated!"
echo ""

# Upgrade pip, setuptools, wheel
echo "Step 1: Upgrading pip, setuptools, and wheel"
echo "----------------------------------------"
python -m pip install --upgrade pip setuptools wheel

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} pip, setuptools, and wheel upgraded!"
else
    echo -e "${RED}✗${NC} Failed to upgrade pip tools!"
    exit 1
fi

echo ""

# Show current package versions
echo "Step 2: Current installed packages"
echo "----------------------------------------"
pip list | head -20
echo "... (showing first 20 packages)"
echo ""

# Upgrade all packages from requirements.txt
echo "Step 3: Upgrading packages from requirements.txt"
echo "----------------------------------------"
pip install --upgrade -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All packages upgraded!"
else
    echo -e "${RED}✗${NC} Some packages failed to upgrade!"
    echo ""
    echo "Trying alternative approach..."
    pip install -r requirements.txt
fi

echo ""

# Verify critical packages
echo "Step 4: Verifying critical packages"
echo "----------------------------------------"

CRITICAL_PACKAGES=("streamlit" "pandas" "numpy" "plotly" "duckdb")

for package in "${CRITICAL_PACKAGES[@]}"; do
    VERSION=$(pip show "$package" 2>/dev/null | grep "Version:" | cut -d' ' -f2)
    if [ -n "$VERSION" ]; then
        echo -e "${GREEN}✓${NC} $package version $VERSION"
    else
        echo -e "${RED}✗${NC} $package not installed!"
    fi
done

echo ""

# Show updated package versions
echo "Step 5: Updated package summary"
echo "----------------------------------------"
echo "Total packages installed: $(pip list | wc -l)"
echo ""
echo "Key packages:"
pip list | grep -E "streamlit|pandas|numpy|plotly|duckdb|streamlit-aggrid"
echo ""

# Check for outdated packages
echo "Step 6: Checking for remaining outdated packages"
echo "----------------------------------------"
OUTDATED=$(pip list --outdated 2>/dev/null | wc -l)

if [ "$OUTDATED" -gt 0 ]; then
    echo -e "${YELLOW}⚠${NC} Found $OUTDATED outdated packages:"
    pip list --outdated | head -10
    if [ "$OUTDATED" -gt 10 ]; then
        echo "... (showing first 10)"
    fi
else
    echo -e "${GREEN}✓${NC} All packages are up to date!"
fi

echo ""

# Generate requirements-lock.txt with exact versions
echo "Step 7: Generating requirements-lock.txt"
echo "----------------------------------------"
pip freeze > requirements-lock.txt
echo -e "${GREEN}✓${NC} requirements-lock.txt created with exact versions"
echo ""

# Summary
echo "========================================"
echo "UPGRADE COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Test the application:"
echo "     streamlit run streamlit_app.py"
echo ""
echo "  2. If everything works, commit the changes:"
echo "     git add requirements.txt requirements-lock.txt"
echo "     git commit -m \"chore: upgrade dependencies to latest versions\""
echo ""
echo "  3. Rebuild Docker image:"
echo "     docker build --no-cache -t sip-spse:latest ."
echo ""
echo "Files updated:"
echo "  - requirements.txt (already updated with new minimum versions)"
echo "  - requirements-lock.txt (exact versions installed)"
echo ""
