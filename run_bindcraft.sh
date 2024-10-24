#!/bin/bash
# Get the AlphaFold2 weights
cp /staging/agitter/alphafold_params_2022-12-06.tar ./params
tar -xvf ./params/alphafold_params_2022-12-06.tar --directory ./params

# Unzip the BindCraft code to the directory BindCraft-1.1.0
unzip bindcraft-v1.1.0.zip

# Run BindCraft
python3 -u ./BindCraft-1.1.0/bindcraft.py --settings './PDL1.json' --filters './default_filters.json' --advanced './4stage_multimer.json'

# Clean up AlphaFold2 weights
rm -rf ./params

# Remove BindCraft code
rm -rf ./BindCraft-1.1.0
