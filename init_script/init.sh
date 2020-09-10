#!/bin/bash

# Check if python exists
# Find biggest Python3 version
# Check if pipenv installed. Install it otherwise
# Run pipenv --python [found version]
# Download the sample program

echo "Checking dependencies..."

PYTHON="NOT FOUND"
python3.9 --version >/dev/null 2>&1
if [ $? -eq 0 ]; then
  PYTHON="python3.9"
else
  python3.8 --version >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    PYTHON="python3.8"
  else
    python3.7 --version >/dev/null 2>&1
    if [ $? -eq 0 ]; then
      PYTHON="python3.7"
    else
      echo "Could not find suitable Python version."
      echo "I need Python 3.7 or later."
      exit 10
    fi
  fi
fi

PIP="NOT FOUND"
pip3 --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
  PIP="pip3"
else
  pip --version > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    PIP="pip"
  else
    echo "Could not find 'pip' command."
    echo "Please ensure 'pip' or 'pip3' command exists on your system and is in the PATH."
    exit 20
  fi
fi

pipenv --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  set -e
  echo "Installing 'pipenv'..."
  cmd=($PIP install pipenv)
  "${cmd[@]}"
  set +e
fi

echo "Creating the project..."
set -e
pipenv --python $PYTHON
pipenv install octopus-sensing
set +e

echo "Downloading sample code..."

MAIN_PY_URL=https://raw.githubusercontent.com/nastaran62/octopus-sensing/master/init_script/main.py

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

echo "Done."
