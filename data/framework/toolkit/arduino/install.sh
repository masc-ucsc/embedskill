#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Arduino CLI Toolkit Installer ==="
echo "Installation directory: $SCRIPT_DIR"
echo ""

# Detect OS and architecture
OS_TYPE=$(uname -s)
ARCH_TYPE=$(uname -m)

if [ "$OS_TYPE" = "Linux" ]; then
    if [ "$ARCH_TYPE" = "x86_64" ]; then
        PLATFORM="Linux_64bit"
        ARCHIVE="tar.gz"
    elif [ "$ARCH_TYPE" = "aarch64" ]; then
        PLATFORM="Linux_ARM64"
        ARCHIVE="tar.gz"
    elif [ "$ARCH_TYPE" = "armv7l" ]; then
        PLATFORM="Linux_ARMv7"
        ARCHIVE="tar.gz"
    else
        echo "Error: Unsupported Linux architecture: $ARCH_TYPE"
        exit 1
    fi
elif [ "$OS_TYPE" = "Darwin" ]; then
    if [ "$ARCH_TYPE" = "x86_64" ]; then
        PLATFORM="macOS_64bit"
        ARCHIVE="tar.gz"
    elif [ "$ARCH_TYPE" = "arm64" ]; then
        PLATFORM="macOS_ARM64"
        ARCHIVE="tar.gz"
    else
        echo "Error: Unsupported macOS architecture: $ARCH_TYPE"
        exit 1
    fi
elif [[ "$OS_TYPE" == MINGW* ]] || [[ "$OS_TYPE" == MSYS* ]]; then
    if [ "$ARCH_TYPE" = "x86_64" ]; then
        PLATFORM="Windows_64bit"
        ARCHIVE="zip"
    else
        echo "Error: Unsupported Windows architecture: $ARCH_TYPE"
        exit 1
    fi
else
    echo "Error: Unsupported operating system: $OS_TYPE"
    exit 1
fi

echo "Detected platform: $PLATFORM"
echo ""

# Check for Rosetta 2 on Apple Silicon
if [ "$PLATFORM" = "macOS_ARM64" ]; then
    echo "Checking for Rosetta 2..."
    if ! pkgutil --pkg-info com.apple.pkg.RosettaUpdateAuto &>/dev/null; then
        echo "Notice: You are on an Apple Silicon Mac."
        echo "While the Arduino CLI itself runs natively, many board toolchains (compilers)"
        echo "still require Rosetta 2 to function."
        echo ""
        echo "Attempting to install Rosetta 2..."
        softwareupdate --install-rosetta --agree-to-license
        echo "✓ Rosetta 2 installation attempted"
    else
        echo "✓ Rosetta 2 is already installed"
    fi
    echo ""
fi

# Download Arduino CLI if not already present
if [ ! -f "arduino-cli/arduino-cli" ] && [ ! -f "arduino-cli/arduino-cli.exe" ]; then
    echo "Downloading Arduino CLI (latest version)..."
    
    DOWNLOAD_URL="https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_${PLATFORM}.${ARCHIVE}"
    DOWNLOAD_FILE="arduino-cli_latest_${PLATFORM}.${ARCHIVE}"
    
    echo "Download URL: $DOWNLOAD_URL"
    echo "Saving to: $DOWNLOAD_FILE"
    
    if command -v curl &> /dev/null; then
        if ! curl -L --fail --progress-bar "$DOWNLOAD_URL" -o "$DOWNLOAD_FILE"; then
            echo "Error: Download failed"
            echo "Please check the URL or download manually from:"
            echo "https://github.com/arduino/arduino-cli/releases/"
            exit 1
        fi
    elif command -v wget &> /dev/null; then
        if ! wget --show-progress "$DOWNLOAD_URL" -O "$DOWNLOAD_FILE"; then
            echo "Error: Download failed"
            echo "Please check the URL or download manually from:"
            echo "https://github.com/arduino/arduino-cli/releases/"
            exit 1
        fi
    else
        echo "Error: Neither wget nor curl found"
        exit 1
    fi
    
    echo "Download complete: $DOWNLOAD_FILE"
    
    echo "Extracting Arduino CLI..."
    mkdir -p arduino-cli
    
    if [ "$ARCHIVE" = "tar.gz" ]; then
        tar -xzf "$DOWNLOAD_FILE" -C arduino-cli
    elif [ "$ARCHIVE" = "zip" ]; then
        unzip -q "$DOWNLOAD_FILE" -d arduino-cli
    fi
    
    rm "$DOWNLOAD_FILE"
    
    # Make executable (Unix-like systems)
    if [ -f "arduino-cli/arduino-cli" ]; then
        chmod +x arduino-cli/arduino-cli
    fi
    
    echo "✓ Arduino CLI downloaded and extracted"
else
    echo "Arduino CLI already installed"
fi

# Create local data directory
if [ ! -d ".arduino15" ]; then
    echo "Creating local data directory..."
    mkdir -p .arduino15
    echo "✓ Data directory created"
else
    echo "Data directory already exists"
fi

# Create local config file
echo "Creating configuration file..."
cat > arduino-cli.yaml << EOF
directories:
  data: $SCRIPT_DIR/.arduino15
  downloads: $SCRIPT_DIR/.arduino15/staging
  user: $SCRIPT_DIR
board_manager:
  additional_urls:
    - https://siliconlabs.github.io/arduino/package_arduinosilabs_index.json
    - https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
daemon:
  port: "50051"
library:
  enable_unsafe_install: false
logging:
  level: info
  format: text
metrics:
  enabled: false
EOF

echo "✓ Configuration file created"
echo ""

# Initialize arduino-cli with local config
echo "Initializing Arduino CLI..."
if [ -f "arduino-cli/arduino-cli" ]; then
    CLI_CMD="./arduino-cli/arduino-cli"
else
    CLI_CMD="./arduino-cli/arduino-cli.exe"
fi

$CLI_CMD --config-file arduino-cli.yaml core update-index

echo "✓ Arduino CLI initialized"
echo ""

echo "=== Installation Complete ==="
echo ""
echo "Arduino CLI installed at: $SCRIPT_DIR/arduino-cli/"
echo "Data directory: $SCRIPT_DIR/.arduino15/"
echo "Config file: $SCRIPT_DIR/arduino-cli.yaml"
echo ""
echo "To use Arduino CLI, run:"
echo "  source $SCRIPT_DIR/export.sh"
echo ""
echo "To install board cores later, use:"
echo "  arduino-cli core install arduino:avr"
echo "  arduino-cli core install arduino:samd"
echo "  arduino-cli core install arduino:mbed_nano"
echo "  arduino-cli core install arduino:renesas_uno"
echo ""
