# Run in adaptyv conda environment
# ChatGPT 4o mini assisted

import click
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr


# Modified from https://stackoverflow.com/a/50835066
def corrfunc(x, y, ax=None, **kwargs):
    """Plot the correlation coefficient in the top left hand corner of a plot."""
    r, _ = pearsonr(x, y)
    ax = ax or plt.gca()
    kwargs['color'] = 'black'  # override the color
    ax.annotate(f'ρ = {r:.2f}', xy=(.1, .9), xycoords=ax.transAxes, **kwargs)


@click.command()
@click.option('--infile', '-i', type=str, help='Filename of the input file with a .tsv extension.'
                                               ' Output files will be based on this filename.')
def main(infile):
    """
    Visualize columns in the BindCraft design summary file.
    """
    df = pd.read_csv(infile, sep='\t')
    print(f'Visualizing {len(df)} sequences')

    # Add relevant derived metrics
    df['ESM2_35M_PLL_Norm'] = df['ESM2_35M_PLL'] / df['Length']

    # Select columns to visualize
    vis_cols = ['Length', 'Average_i_pTM', 'Average_i_pAE', 'Average_Binder_Energy_Score', 'ESM2_35M_PLL',
                'ESM2_35M_PLL_Norm', 'METL-G-20M-1D']
    df_selected = df[vis_cols]
    print(df_selected.describe().to_string())

    # Create a pairplot
    g = sns.pairplot(df_selected, corner=True)
    g.map_lower(corrfunc)

    outfile = infile.replace('.tsv', '.png')
    plt.savefig(outfile, dpi=600, bbox_inches='tight')


if __name__ == "__main__":
    main()
