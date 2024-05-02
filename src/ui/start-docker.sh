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
echo "Starting Magisim UI..."
# check if we are in the right conda environment
if [ "$CONDA_DEFAULT_ENV" != "magisim" ]; then
    echo "You are not in the right conda environment. Please activate the magisim environment."
    # are we in a docker container?
    echo "MAGISIM_APP: Docker container detected.\n"
    conda init bash
    source /root/.bashrc
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
uvicorn ui:msim_ui --host 0.0.0.0 --port 8000

# if we are in a docker container, make sure to not exit
echo "Docker container detected. Not exiting."
tail -f /dev/null
