#!/bin/bash
# Script untuk build dan test Docker image
# Usage: ./build-and-test.sh

set -e  # Exit on error

echo "========================================"
echo "SIP-SPSE Docker Build & Test Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if public directory and logo files exist
echo "Step 1: Checking local files..."
echo "----------------------------------------"

if [ -d "public" ]; then
    echo -e "${GREEN}✓${NC} Public directory exists"
else
    echo -e "${RED}✗${NC} Public directory NOT found!"
    exit 1
fi

if [ -f "public/sip-spse.png" ]; then
    SIZE=$(stat -c%s "public/sip-spse.png")
    echo -e "${GREEN}✓${NC} Logo file exists (${SIZE} bytes)"
else
    echo -e "${RED}✗${NC} Logo file NOT found!"
    exit 1
fi

if [ -f "public/sip-spse-icon.png" ]; then
    SIZE=$(stat -c%s "public/sip-spse-icon.png")
    echo -e "${GREEN}✓${NC} Icon file exists (${SIZE} bytes)"
else
    echo -e "${RED}✗${NC} Icon file NOT found!"
    exit 1
fi

echo ""

# Step 2: Build Docker image
echo "Step 2: Building Docker image..."
echo "----------------------------------------"

IMAGE_NAME="sip-spse:test-$(date +%Y%m%d-%H%M%S)"

echo "Building image: ${IMAGE_NAME}"
docker build --progress=plain --no-cache -t "${IMAGE_NAME}" . 2>&1 | tee build.log

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Build successful!"
else
    echo -e "${RED}✗${NC} Build failed! Check build.log for details"
    exit 1
fi

echo ""

# Step 3: Run debug script in container
echo "Step 3: Running debug script in container..."
echo "----------------------------------------"

docker run --rm "${IMAGE_NAME}" python3 debug_docker.py 2>&1 | tee debug_output.txt

echo ""

# Step 4: Test logo paths
echo "Step 4: Testing logo paths..."
echo "----------------------------------------"

docker run --rm "${IMAGE_NAME}" python3 test_logo.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Logo paths test passed!"
else
    echo -e "${RED}✗${NC} Logo paths test failed!"
fi

echo ""

# Step 5: Ask if user wants to run the container
echo "Step 5: Ready to run container"
echo "----------------------------------------"

read -p "Do you want to start the container? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting container on port 8502..."
    echo "Press Ctrl+C to stop"
    echo ""
    docker run --rm -p 8502:8502 --name sip-spse-test "${IMAGE_NAME}"
else
    echo ""
    echo "Container not started."
    echo "To run manually:"
    echo "  docker run -p 8502:8502 ${IMAGE_NAME}"
    echo ""
    echo "To tag as latest:"
    echo "  docker tag ${IMAGE_NAME} sip-spse:latest"
fi

echo ""
echo "========================================"
echo "Build & Test Complete!"
echo "========================================"
echo "Logs saved to:"
echo "  - build.log"
echo "  - debug_output.txt"
echo ""
