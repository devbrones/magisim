#!/bin/sh
# activate-env.sh
# check if environment already exists
if conda env list | grep -q "magisim"; then
    echo "magisim environment already exists, activating..."
    echo "please wait..."
    conda activate magisim
    exit 0
fi
echo "magisim environment does not exist, creating..."
conda env create -f conda-env.yml
echo "please wait..."
sleep 10
conda activate magisim
exit 0





