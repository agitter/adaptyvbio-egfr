#!/bin/bash
# Unpack the BindCraft code to the directory BindCraft-1.1.0
tar -xvf bindcraft-v1.1.0.tar.gz

# Get the AlphaFold2 weights
mkdir -p ./BindCraft-1.1.0/params
cp /staging/agitter/alphafold_params_2022-12-06.tar ./BindCraft-1.1.0/params/
tar -xvf ./BindCraft-1.1.0/params/alphafold_params_2022-12-06.tar --directory ./BindCraft-1.1.0/params

chmod u+x ./BindCraft-1.1.0/functions/dssp
chmod u+x ./BindCraft-1.1.0/functions/DAlphaBall.gcc

# Run BindCraft
python3 -u ./BindCraft-1.1.0/bindcraft.py --settings "./EGFR_${settings}.json" --filters "./default_filters_${filters}.json" --advanced "./4stage_multimer_${advanced}.json"

# Tar the output
tar -czf EGFR_output_${cluster}_${process}.tgz ./EGFR_output

# Remove BindCraft code and AlphaFold2 weights
rm -rf ./BindCraft-1.1.0