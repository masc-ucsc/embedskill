#!/bin/bash

# This script must be sourced, not executed
if [[ "$0" == "${BASH_SOURCE[0]}" ]] || [[ "$0" == "$1" ]]; then
    echo "Error: This script must be sourced, not executed!"
    echo "Usage: source /path/to/export.sh"
    exit 1
fi

# Detect script path (compatible with Bash and Zsh)
if [ -n "$BASH_SOURCE" ]; then
    SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "$ZSH_VERSION" ]; then
    SCRIPT_PATH="${(%):-%x}"
else
    SCRIPT_PATH="$0"
fi

SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"

# Check if installation has been run
if [ ! -d "$SCRIPT_DIR/arduino-cli" ]; then
    echo "Error: Arduino CLI not installed. Please run ./install.sh first"
    return 1
fi

if [ ! -f "$SCRIPT_DIR/arduino-cli.yaml" ]; then
    echo "Error: Configuration file not found. Please run ./install.sh first"
    return 1
fi

# Set environment variables
export ARDUINO_TOOLKIT_ROOT="$SCRIPT_DIR"
export ARDUINO_CLI_CONFIG="$SCRIPT_DIR/arduino-cli.yaml"
export ARDUINO_DATA_DIR="$SCRIPT_DIR/.arduino15"

# Add arduino-cli to PATH
export PATH="$SCRIPT_DIR/arduino-cli:$PATH"

# Create helpful aliases
alias acompile='arduino-cli compile'
alias aupload='arduino-cli upload'
alias amonitor='arduino-cli monitor'
alias aboard='arduino-cli board'
alias acore='arduino-cli core'
alias alib='arduino-cli lib'

echo "Arduino CLI Toolkit activated!"
echo "  Toolkit root: $ARDUINO_TOOLKIT_ROOT"
echo "  Config file: $ARDUINO_CLI_CONFIG"
echo "  Data directory: $ARDUINO_DATA_DIR"
echo ""

# Show arduino-cli version
arduino-cli version 2>/dev/null || echo "Warning: arduino-cli not found in PATH"

echo ""
echo "Helpful aliases:"
echo "  acompile  - Compile sketches"
echo "  aupload   - Upload to board"
echo "  amonitor  - Serial monitor"
echo "  aboard    - Board management"
echo "  acore     - Core management"
echo "  alib      - Library management"
echo ""
echo "Common commands:"
echo "  arduino-cli board list"
echo "  arduino-cli core install arduino:avr"
echo "  arduino-cli compile --fqbn arduino:avr:uno /path/to/sketch"
echo "  arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno /path/to/sketch"
echo ""
