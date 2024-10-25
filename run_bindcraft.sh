#!/bin/bash
# Unpack the BindCraft code to the directory BindCraft-1.1.0
tar -xvf bindcraft-v1.1.0.tar.gz

# Get the AlphaFold2 weights
mkdir -p ./BindCraft-1.1.0/params
cp /staging/agitter/alphafold_params_2022-12-06.tar ./BindCraft-1.1.0/params/
tar -xvf ./BindCraft-1.1.0/params/alphafold_params_2022-12-06.tar --directory ./BindCraft-1.1.0/params

# Run BindCraft
python3 -u ./BindCraft-1.1.0/bindcraft.py --settings './PDL1.json' --filters './default_filters.json' --advanced './4stage_multimer.json'

# Remove BindCraft code and AlphaFold2 weights
rm -rf ./BindCraft-1.1.0
