#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
PYTHON_BIN="${PYTHON_BIN:-python3.13}"

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "Requested Python interpreter '${PYTHON_BIN}' not found."
  if command -v python3.13 >/dev/null 2>&1; then
    PYTHON_BIN="python3.13"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    echo "No suitable Python interpreter found."
    exit 1
  fi
fi

echo "Creating virtual environment in ${VENV_DIR} using ${PYTHON_BIN}..."
"${PYTHON_BIN}" -m venv "${VENV_DIR}"

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required packages..."
pip install pygame click

echo
echo "Setup completed."
echo "Activate environment with: source ${VENV_DIR}/bin/activate"
echo "Run GUI with: python3 path_finding_gui.py -f maps/map_1.json"
