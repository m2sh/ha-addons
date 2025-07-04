#!/bin/sh
# ==============================================================================
# Home Assistant Add-on: Chisel
#
# Container build of Chisel
# ==============================================================================

set -e

# Machine architecture as first parameter
arch=$1

# Chisel release as second parameter
chiselRelease=$2

echo "Build script started with arch=$arch, release=$chiselRelease"
echo "Current architecture: $(uname -m)"
echo "Current platform: $(uname -a)"

# Adapt the architecture to the chisel specific names if needed
# see HA Archs: https://developers.home-assistant.io/docs/add-ons/configuration/#:~:text=the%20add%2Don.-,arch,-list
# see Chisel Archs: https://github.com/jpillora/chisel/releases
case $arch in
    "aarch64")
        arch="arm64"
        echo "Mapped aarch64 to arm64"
    ;;

    "armv7")
        arch="armv7"
        echo "Keeping armv7 as armv7"
    ;;
esac

echo "Final architecture for download: $arch"

# Download the chisel binary
echo "Downloading Chisel v${chiselRelease} for ${arch}..."
wget -O /tmp/chisel.gz "https://github.com/jpillora/chisel/releases/download/v${chiselRelease}/chisel_${chiselRelease}_linux_${arch}.gz"

# Check if download was successful
if [ ! -f "/tmp/chisel.gz" ]; then
    echo "ERROR: Failed to download chisel binary"
    exit 1
fi

echo "Download successful, file size: $(ls -la /tmp/chisel.gz)"

# Extract the gzipped binary
echo "Extracting Chisel binary..."
gunzip /tmp/chisel.gz

# Check if extraction was successful
if [ ! -f "/tmp/chisel" ]; then
    echo "ERROR: Failed to extract chisel binary"
    exit 1
fi

echo "Extraction successful, file size: $(ls -la /tmp/chisel)"

# Move the extracted binary to the correct location
mv /tmp/chisel /usr/bin/chisel

# Make the downloaded binary executable
chmod +x /usr/bin/chisel

# Verify the binary works
echo "Verifying Chisel binary..."
if ! /usr/bin/chisel --version; then
    echo "ERROR: Chisel binary verification failed"
    echo "Binary details:"
    file /usr/bin/chisel
    ldd /usr/bin/chisel 2>/dev/null || echo "ldd not available or binary is statically linked"
    exit 1
fi

# Remove legacy cont-init.d services (if they exist)
if [ -d "/etc/cont-init.d" ]; then
    echo "Removing legacy cont-init.d directory"
    rm -rf /etc/cont-init.d
fi

# Remove s-6 legacy/deprecated (and not needed) services (if they exist)
if [ -f "/package/admin/s6-overlay/etc/s6-rc/sources/base/contents.d/legacy-cont-init" ]; then
    echo "Removing legacy-cont-init file"
    rm /package/admin/s6-overlay/etc/s6-rc/sources/base/contents.d/legacy-cont-init
fi

if [ -f "/package/admin/s6-overlay/etc/s6-rc/sources/base/contents.d/fix-attrs" ]; then
    echo "Removing fix-attrs file"
    rm /package/admin/s6-overlay/etc/s6-rc/sources/base/contents.d/fix-attrs
fi

if [ -f "/package/admin/s6-overlay/etc/s6-rc/sources/top/contents.d/legacy-services" ]; then
    echo "Removing legacy-services file"
    rm /package/admin/s6-overlay/etc/s6-rc/sources/top/contents.d/legacy-services
fi

echo "Chisel installation completed successfully!" 