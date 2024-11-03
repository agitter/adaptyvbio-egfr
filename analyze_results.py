# Run in adaptyv conda environment
# ChatGPT 4o mini assisted

import glob

import click
import metl
import pandas as pd
import torch

from competition_metrics.compute_pll import compute_pll

# Hard code the METL model identifier
# https://github.com/gitter-lab/metl-pretrained?tab=readme-ov-file#global-source-models
METL_MODEL_ID = 'METL-G-20M-1D'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def add_metl_scores(df, batch_size=1):
    """
    Score METL sequences in batches
    @param df: dataframe with Sequence column
    @param batch_size: batch size for scoring METL sequences
    """
    metl_model, metl_data_encoder = metl.get_from_ident(METL_MODEL_ID)
    metl_model.eval()
    metl_model = metl_model.to(device)

    scores = []  # List to store scores

    # Process sequences in batches
    for start in range(0, len(df), batch_size):
        end = min(start + batch_size, len(df))
        batch_sequences = df['Sequence'].iloc[start:end].tolist()
        encoded_seqs = metl_data_encoder.encode_sequences(batch_sequences)

        with torch.no_grad():
            predictions = metl_model(torch.tensor(encoded_seqs))

        # Extract the first element of each prediction: total_score
        scores.extend(predictions[:, 0].tolist())

    # Add scores to the DataFrame
    df['METL-G-20M-1D'] = scores

    return df


@click.command()
@click.option('--output', '-o', type=str, help='Filename of the output file without the .tsv extension.'
                                               ' Will be written in the results directory')
def main(output):
    """
    Process the final_design_stats.csv output files from BindCraft by merging them, adding ESM2 650M PLL and
    METL-G-20M-1D scores, and writing summary .tsv files.
    """
    # Define the pattern to match the CSV files
    pattern = 'results/EGFR_output*/final_design_stats.csv'

    # Use glob to find all matching CSV files
    bindcraft_csvs = glob.glob(pattern)

    # Initialize an empty list to store DataFrames
    dataframes = []

    # Iterate over the list of CSV files
    for csv_file in bindcraft_csvs:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Append the DataFrame to the list
        dataframes.append(df)

    # Concatenate all DataFrames into a single DataFrame
    concat_df = pd.concat(dataframes, ignore_index=True)

    concat_df = concat_df[:25]

    # Add ESM2 35M PLL scores for each sequence
    # concat_df['ESM2_650M_PLL'] = concat_df['Sequence'].apply(compute_pll, model_type='650M')
    # concat_df['ESM2_150M_PLL'] = concat_df['Sequence'].apply(compute_pll, model_type='150M')
    # concat_df['ESM2_35M_PLL'] = concat_df['Sequence'].apply(compute_pll, model_type='35M')

    # Add METL Global scores for each sequence
    concat_df = add_metl_scores(concat_df, batch_size=1)

    output = f'results/{output}.tsv'
    concat_df.to_csv(output, sep='\t', index=False)

    print(f"Wrote summary file: {output}")


if __name__ == "__main__":
    main()
