#!/bin/bash

# Check if python exists
# Find biggest Python3 version
# Check if pipenv installed. Install it otherwise
# Run pipenv --python [found version]
# Download the sample program

echo "Checking dependencies..."

function check_python {
  VERSION=$1
  python$VERSION --version >/dev/null 2>&1
  return $?
}

PYTHON="NOT FOUND"

if check_python 3.13; then
  PYTHON="python3.13"
else
  if check_python 3.12; then
    PYTHON="python3.12"
  else
    if check_python 3.11; then
      PYTHON="python3.11"
    else
      if check_python 3.10; then
        PYTHON="python3.10"
      else
        echo "Could not find suitable Python version."
        echo "I need Python 3.10 or later."
        exit 10
      fi
    fi
  fi
fi

PIP="NOT FOUND"
$PYTHON -m pip --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
  PIP="pip3"
else
  echo "$PYTHON doesn't have the 'pip' module"
  echo "Please ensure you installed 'pip' for this version of Python"
  exit 20
fi

pipenv --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  set -e
  echo
  echo "Couldn't find pipenv on you system. Do you want me to install it?"
  ANSWER=""
  read -p "[y/n]" -N 1 ANSWER
  if [[ $ANSWER != "y" && $ANSWER != "Y" ]]; then
    echo "Please install 'pipenv' and run the script again"
    exit 0
  fi
  echo "Installing 'pipenv'..."
  # Checking if there's a sudo command on this machine.
  SUDO_CMD=""
  sudo --help > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    SUDO_CMD="sudo"
  fi
  $SUDO_CMD $PIP install pipenv
  set +e
fi

echo
echo "Creating the project. Going to use:"
$PYTHON --version
$PIP --version
pipenv --version
echo

set -e
pipenv --python $PYTHON
pipenv install "octopus-sensing[camera]" octopus-sensing-monitoring octopus-sensing-visualizer
set +e

echo "Downloading sample code..."

MAIN_PY_URL=https://raw.githubusercontent.com/octopus-sensing/octopus-sensing/master/examples/add_sensors.py

curl --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
  set -e
  curl --output main.py $MAIN_PY_URL
  set +e
else
  wget --version >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    set -e
    wget $MAIN_PY_URL
    set +e
  else
    echo "Could not download the sample code."
    echo "I need 'curl' or 'wget' to download it."
    exit 30
  fi
fi

echo
echo "Done."
