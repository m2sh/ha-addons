#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if addon name is provided
if [ -z "$1" ]; then
    print_error "Usage: $0 <addon-name>"
    print_error "Example: $0 chisel"
    exit 1
fi

ADDON_NAME=$1
ADDON_DIR="./$ADDON_NAME"

# Check if addon directory exists
if [ ! -d "$ADDON_DIR" ]; then
    print_error "Addon directory '$ADDON_DIR' does not exist"
    exit 1
fi

print_status "Building addon: $ADDON_NAME"

# Change to addon directory
cd "$ADDON_DIR"

# Check if build.yaml exists
if [ ! -f "build.yaml" ]; then
    print_error "build.yaml not found in $ADDON_DIR"
    exit 1
fi

# Build the addon using docker
print_status "Starting build process..."
docker build \
    --build-arg BUILD_FROM=ghcr.io/hassio-addons/base/amd64:14.0.0 \
    --build-arg BUILD_ARCH=amd64 \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg BUILD_DESCRIPTION="$(grep '^description:' config.yaml | cut -d' ' -f2-)" \
    --build-arg BUILD_NAME="$(grep '^name:' config.yaml | cut -d' ' -f2-)" \
    --build-arg BUILD_REF="$(git rev-parse HEAD)" \
    --build-arg BUILD_REPOSITORY="m2sh/ha-addons" \
    --build-arg BUILD_VERSION="$(grep '^version:' config.yaml | cut -d' ' -f2-)" \
    -t "local/$ADDON_NAME:latest" \
    .

print_status "Build completed successfully!"
print_status "You can test the addon locally with:"
print_status "docker run -it --rm local/$ADDON_NAME:latest" 