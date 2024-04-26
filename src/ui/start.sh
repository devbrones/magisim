#!/bin/sh
# Magisim Start Script (c) 2024, Magisim Team under LGPLv3


## PREFLIGHT CHECKS
# check if we are in the right directory
if [ ! -f "ui.py" ]; then
    echo "You are not in the right directory. Please run this script from the /src/ui directory of the project."
    exit 1
fi

# check if the log is too big
if [ -f "ui.log" ]; then
    if [ $(wc -l < "ui.log") -gt 1000 ]; then
        echo "ui.log is too big. Truncating..."
        echo "" > ui.log
    fi
fi

# check if we are in the right conda environment
if [ "$CONDA_DEFAULT_ENV" != "magisim" ]; then
    echo "You are not in the right conda environment. Please activate the magisim environment."
    # are we in a docker container?
    if [ -f "/.dockerenv" ]; then
        echo "Docker container detected."
        conda init bash
    else
        continue
    fi
    conda activate magisim
fi

# check if redis is running
if ! pgrep -x "redis-server" > /dev/null
then
    echo "Redis is not running. Starting redis..."
    redis-server &
else
    echo "Redis is already running."
fi

# start using uvicorn
uvicorn ui:msim_ui