#!/bin/sh
#

# start using uvicorn
echo "Make sure you are in the magisim conda environment."
uvicorn ui:fapp --reload --port $(python -c "from shared import config; print(config.Config.UI.port)") 
