#!/bin/sh
#

# start using uvicorn
echo "Make sure you are in the magisim conda environment."
redis-server
uvicorn ui:fapp
