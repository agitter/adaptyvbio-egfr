#!/bin/bash
# ChatGPT 4o mini assisted

# Run from the directory containing the script
# Extracts the BindCraft results and renames the extracted directory to retain
# the cluster and process job IDs
input_dir=results

# Iterate over each tarball in the results directory that matches the pattern
for tarball in "$input_dir"/EGFR_output_*.tgz; do
    # Extract the cluster and process indices from the filename with regex
    if [[ "$tarball" =~ EGFR_output_([^_]+)_([^_]+)\.tgz ]]; then
        cluster="${BASH_REMATCH[1]}"
        process="${BASH_REMATCH[2]}"
        
        new_directory="${input_dir}/EGFR_output_${cluster}_${process}"

        # Check if the output directory already exists
        if [ -d "$new_directory" ]; then
            echo "Directory $new_directory already exists. Skipping $tarball."
            continue  # Skip to the next iteration
        fi

        # Extract the tarball
        tar -xzf "$tarball" -C "$input_dir"

        # Output directory to rename
        old_directory="${input_dir}/EGFR_output"

        if [ -d "$old_directory" ]; then
            mv "$old_directory" "$new_directory"
            echo "Renamed $old_directory to $new_directory"
        else
            echo "Directory $old_directory does not exist after extracting $tarball."
        fi
    else
        echo "Filename $tarball does not match expected pattern."
    fi
done
