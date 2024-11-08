# Adaptyv EGFR protein design competition round 2

## Strategy
"If you can't beat 'em, join 'em".
My overall strategy was to build on top of BindCraft based on its strong [round 1](https://www.adaptyvbio.com/blog/po102) performance and impressive [preprint](https://doi.org/10.1101/2024.09.30.615802).
However, beyond using BindCraft to generate sequences there were several competing objectives:
- Do something besides pure BindCraft to inject some "creativity" into the ranking or filtering
- Balance the goals of having sequences selected for experimental testing (via top 100 ranking or creativity criteria) with generating strong binders that are likely to express

Regarding the latter, the ranking metrics prioritized short sequences because the pseudo-log-likelihood (PLL) is not length normalized.
Should I bias my BindCraft settings toward short sequences, or would that hurt success in the lab?
The round 1 winner `martin.pacesa-EGFR_l138_s90285_mpnn2` had length 138 and a ESM2 650M PLL of -320.68, which would put it at risk of falling out of the top 100 in round 2!

I decided to try multiple BindCraft settings and score the generated sequences with ESM2 PLL and our own biophysics-based protein language model [METL](https://doi.org/10.1101/2024.03.15.585128).
We know METL-Global has problems generalizing to all protein folds, but I also expected no one else would use it (creativity points!) and couldn't resist the opportunity for some self-promotion.

## Lessons learned
BindCraft was fairly easy to run in my local research computing facility (CHTC) given the complexity of the underlying model.
I did not initially anticipate how much GPU memory and time it would require when running with the full EGFR sequence as input.
I wasted time with failed jobs that ran out of GPU memory or hit runtime limits.

I was slightly dismayed by the aesthetics of my designs.
My final submissions were all bland: small, helical predicted structures.
I tried penalizing helicity in a few runs, but didn't explore that deeply, and those results were not my best-scoring sequences.
I did include some in my initial submissions.
I'm jealous of the [solenoid](https://x.com/_judewells/status/1853805798641541625) Jude Wells showed.
Maybe elegance can be part of the selection process for the second set of 100.

Besides those minor gripes, running BindCraft was pleasant.
It was easy to configure and explore the design space and run in a high-throughput setting.
It computed and reported a lot of metrics I was interested in so I only added ESM2 PLL and the METL score myself.

BindCraft may not be capable of maximizing iPTM and minimizing iPAE as much as an algorithm that only optimizes those scores.
That is likely bad for climbing the leaderboard but good for designing functional proteins.
Some of my observations about aesthetics, iPTM, and iPAE may be due to choices I made about BindCraft settings and not the tool itself.

Ultimately, Adaptyv [doubled](https://adaptyvbio.substack.com/p/protein-design-competition-update) the number of experimentally tested proteins and selected 1-5 sequences per participant who submitted a description.
This was a fair way to address concerns about overfitting to the leaderboard metrics, which they were already [thinking about](https://x.com/TheGermanPole/status/1854837263563165963).
Had I known I was not going to make it into the top 100 and would still have some sequences tested, I might have tried more long sequences and prioritized PLL a little less.

## Overall organization
- BindCraft runs in an Apptainer container on GPUs in the UW-Madison research computing facility with jobs managed by HTCondor.
- Local analysis code runs on CPU in a conda environment to collect and visualize the BindCraft results.
- A few intermediate submissions gave partial feedback about which sequences ranked well and which strategies worked well.

## Building BindCraft
I built the Apptainer container with an interactive CHTC job following their [instructions](https://chtc.cs.wisc.edu/uw-research-computing/apptainer-htc) and the submit file `build_bindcraft.sub`.
This was submitted with `condor_submit -i build_bindcraft.sub`.

Within the interactive job, I ran
```
chmod 1777 /tmp
apptainer build bindcraft.sif bindcraft.def
mv bindcraft.sif /staging/agitter
```
`chmod` was needed to address errors related to [temporary files](https://superuser.com/questions/1496529/sudo-apt-get-update-couldnt-create-temporary-file) encountered during the container build (see below).

The container does not include the actual BindCraft source code, so that was downloaded separately and transferred to jobs.
BindCraft v1.1.0 was downloaded with
```
wget -O bindcraft-v1.1.0.tar.gz https://github.com/martinpacesa/BindCraft/archive/refs/tags/v1.1.0.tar.gz
```

## AlphaFold2 weights
The AlphaFold2 weights were downloaded and copied to [CHTC staging](https://chtc.cs.wisc.edu/uw-research-computing/file-avail-largedata.html)
```
curl -o params/alphafold_params_2022-12-06.tar https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
cd params/
$ scp alphafold_params_2022-12-06.tar agitter@transfer.chtc.wisc.edu:/staging/agitter/
```

## BindCraft EGFR settings
The structure (PDB [6ARU](https://www.rcsb.org/structure/6aru)) and interaction sites are those provided by [Adaptyv](https://design.adaptyvbio.com/).
A different HTCondor submission file `run_bindcraft_EGFR_<n>.sub` was used for each of the settings below with the same executable script `run_bindcraft_EGFR.sh`.
Environment variables controlled which BindCraft settings in the `EGFR` subdirectory were passed to the script.
1. Default BindCraft filters and advanced settings. All interaction sites from Adaptyv. Lengths 50 to 250.
2. Default BindCraft filters and advanced settings. Domain 3 structure without interaction sites. Lengths 60 to 120. Strategy from [@design_proteins](https://x.com/design_proteins/status/1851295516564525515) and structure from [@btnaughton](https://x.com/btnaughton/status/1851436952446537980).
3. Default BindCraft filters and advanced settings. Domain 3 structure without interaction sites. Lengths 50 to 75. Modifies strategy 2 with shorter lengths.
4. Default BindCraft filters. Modify advanced settings to increase `weights_pae_inter` and `weights_iptm` 4x. Domain 3 structure without interaction sites. Lengths 60 to 120.
5. Default BindCraft filters. Modify advanced settings to increase `weights_pae_inter` and `weights_iptm` 4x and `weights_helicity` to -1. Domain 3 structure without interaction sites. Lengths 60 to 120.
6. Default BindCraft filters and advanced settings. All interaction sites from Adaptyv. Lengths 50 to 200. Similar to setting 1 but reconfigured into a larger number of shorter jobs and shortened max length. Reduced iterations to reduce runtime.
7. Default BindCraft filters. Modify advanced settings to increase `weights_pae_inter` and `weights_iptm` 4x. Domain 3 structure with interaction sites. Lengths 60 to 120.
8. Default BindCraft filters and advanced settings. All interaction sites from Adaptyv. Lengths 50 to 200. Similar to setting 6 but further reduced iterations to reduce runtime.
9. Default BindCraft filters and advanced settings. All interaction sites from Adaptyv. Lengths 50 to 200. Similar to setting 1 but reconfigured into a single design per job and increased max allowed runtime. Post-competition.

Several of these settings did not produce any sequences because the jobs timed out or did not finish before the competition deadline.

## Analysis
The analysis code runs in the `adaptyv` conda environment created with `environment.yml`.
It was derived from the [METL](https://github.com/gitter-lab/metl/blob/9912989380ebe1246a2e35a92488e424d7ae571b/environment.yml) environment to be compatible with METL pretrained models and updated to add requirements for the Adaptyv `competition_metrics`.
After creating and activating the environment, `pip install metl-pretrained/` to install the local METL package.

`round2-esm2-pll-check.tsv` is an intermediate file with ESM2 PLLs from the 35M, 150M, and 650M models for 25 round 2 sequences.
It was used to assess if the smaller models could be used to compute PLL for ranking and filtering so that the PLL could be computed on CPU for convenience.
The Pearson correlation of the smaller models with the 650M model is > 0.98.

## Submissions
### Submission 1
After the [announcement](https://x.com/adaptyvbio/status/1852435680506355823) that "You can also submit more than once but we will only count the last 10 designs for the leaderboard", I made an initial submission on 2024-11-01 before the full pipeline was finished to get initial feedback.
This submission collected all BindCraft designs with the ChatGPT 4o mini-suggested command
```
find . -type f -path './EGFR_output_*/*final_design_stats.csv' -exec cat {} + > round2_concatenated_final_design_stats_sub1.csv
```
That file was manually reviewed to:
- Prioritize Average_i_pTM
- Use Average_i_pAE and Average_pLDDT as secondary criteria
- Select sequences from unique seeds
- Select two sequences from runs with `weights_helicity` -1.0

The resulting 10 sequences are `round2-egfr-inhibitors-submission1-key.fasta` and an anonymized version is `round2-egfr-inhibitors-submission1.fasta` that strips the BindCraft design names.
On 2024-11-02, the results were [saved](results/round2-egfr-inhibitors-submission1-leaderboard-2024-11-02.png).

### Submission 2
The second submission focused on short sequences. I generated `round2_concatenated_final_design_stats_sub1.csv` using the additional BindCraft runs that had finished and manually reviewed the file using the same criteria as before.
This time I required the general sequences to have length <= 60 and the non-helical sequences to have length <= 75 (none were run with allowed lengths <= 60).
The resulting 10 sequences are `round2-egfr-inhibitors-submission2-key.fasta` and `round2-egfr-inhibitors-submission2.fasta`.
On 2024-11-04, the results were [saved](results/round2-egfr-inhibitors-submission2-leaderboard-2024-11-04.png).

### Submission 3
The third submission added additional scores to the BindCraft designs: [ESM2](https://github.com/facebookresearch/esm) 35M PLL and [METL-Global](https://github.com/gitter-lab/metl-pretrained) 20M 1D approximation of [Rosetta](https://rosettacommons.org/) total score.
A new script collects the BindCraft designs and generates these scores:
```
python analyze_results.py -o round2_concatenated_final_design_stats_sub3
```
to create `results/round2_concatenated_final_design_stats_sub3.tsv`.

That file was manually reviewed to select five sequences with unique seeds that have the best (lowest) `METL-G-20M-1D` score, which is a standardized Rosetta total_score.
The other five sequences were those with unique seeds that have the best (highest) `ESM2_35M_PLL` score.
This was not length normalized, so they are all very short sequences.
The resulting 10 sequences are `round2-egfr-inhibitors-submission3-key.fasta` and `round2-egfr-inhibitors-submission3.fasta`.

I did not receive results for this submission after 24 hours and made submission 4 without that feedback.

### Submission 4 - final submission
No additional BindCraft runs finished before the deadline, so the fourth and final submission is also based on `results/round2_concatenated_final_design_stats_sub3.tsv`.
I added visualizations of key sequences metrics using
```
python visualize_results.py -i results/round2_concatenated_final_design_stats_sub3.tsv
```
to create `results/round2_concatenated_final_design_stats_sub3.png`
The script also prints summary statistics that were used for filtering:
```
           Length  Average_i_pTM  Average_i_pAE  Average_Binder_Energy_Score  ESM2_35M_PLL  ESM2_35M_PLL_Norm  METL-G-20M-1D
count  675.000000     675.000000     675.000000                   675.000000    675.000000         675.000000     675.000000
mean    86.149630       0.769304       0.215111                  -228.684193   -209.928286          -2.438040       3.452004
std     19.470357       0.064124       0.051408                    57.451657     48.700573           0.159236       1.006219
min     50.000000       0.580000       0.120000                  -399.490000   -314.912308          -2.904612       1.031595
25%     70.000000       0.720000       0.170000                  -275.770000   -247.211050          -2.545492       2.754379
50%     86.000000       0.780000       0.210000                  -224.390000   -209.866245          -2.446161       3.411098
75%    104.000000       0.820000       0.250000                  -179.920000   -169.663794          -2.343204       4.166741
max    120.000000       0.890000       0.340000                  -111.350000   -100.935247          -1.711663       6.880487
```

The 675 sequences were then filtered:
- Eliminate those with the BindCraft `Notes` "Relaxed structure contains clashes".
- `Average_i_pTM` >= 0.82 (75th percentile)
- `Average_i_pAE` <= 0.17 (25th percentile)
- `ESM2_35M_PLL` >= -169.663794 (75th percentile)
- `METL-G-20M-1D` <= 4.166741 (75th percentile)
- `Average_Binder_Energy_Score` >= -179.92 (75th percentile)

The 18 remaining sequences were saved as `results/round2_concatenated_final_design_stats_sub4.tsv`.
EGFR_l54_s382790_mpnn8 (yolo23) from submission 2 was still in this subset and ranked fairly well, so it was selected.
EGFR_l80_s42487_mpnn1 (yolo17) from submission 1 was not in this subset, but it was also selected because it ranked fairly well and had no clashes.
EGFR_l61_s584422_mpnn3 was selected because it was the only remaining sequence that specified a `Target_Hotspot`.

The next four sequences maximized `Average_i_pTM` (skipping over EGFR_l60_s632945_mpnn4 that was tested in submission 2 and did not rank in the top 100): EGFR_l62_s815249_mpnn2, EGFR_l62_s958143_mpnn2, EGFR_l62_s958143_mpnn1, and EGFR_l62_s954907_mpnn6.
These happened to be the sequences that also minimized `Average_i_pAE`.

The final three sequences maximized `ESM2_35M_PLL` (skipping over EGFR_l51_s672443_mpnn3 and EGFR_l52_s649556_mpnn10 that were tested in submission 2 and did not rank in the top 100): EGFR_l54_s733980_mpnn1, EGFR_l62_s954907_mpnn3, and EGFR_l63_s786397_mpnn2.

I inspected the structures output from BindCraft in the [Mol* 3D Viewer](https://www.rcsb.org/3d-view), aligned them on [UniProt](https://www.uniprot.org/align), and ran [BLAST](https://www.uniprot.org/blast) on UniProt to confirm low similarity to natural proteins.

EGFR_l54_s382790_mpnn8 (yolo23), EGFR_l54_s733980_mpnn1 (yolo46), and EGFR_l63_s786397_mpnn2 (yolo48) were selected for [experimental testing](https://foundry.adaptyvbio.com/egfr_design_competition_2)!

## Third-party files
- `bindcraft.def`: Apptainer Definition file created by [@komatsuna-san](https://github.com/martinpacesa/BindCraft/issues/23#issuecomment-2408333526).
- `bindcraft-v1.1.0.tar.gz`: BindCraft [v1.1.0 release](https://github.com/martinpacesa/BindCraft/releases/tag/v1.1.0) archive. Available under the [MIT License](https://github.com/martinpacesa/BindCraft/blob/main/LICENSE).
- `PDL1_example`: BindCraft example files in this subdirectory are from its [GitHub repo](https://github.com/martinpacesa/BindCraft/tree/d2d3cd0b5d6b02d12d24afa59e640717e36f552c) (version 1.1.0). Available under the [MIT License](https://github.com/martinpacesa/BindCraft/blob/main/LICENSE).
- `6aru.pdb`: Structure of Cetuximab Fab mutant in complex with EGFR extracellular domain (PDB [6ARU](https://www.rcsb.org/structure/6aru))
- `6aru_final_chain_A_domain_3.pdb`: Domain 3 of EGFR structure [6ARU](https://www.rcsb.org/structure/6aru) from @btnaughton's [gist](https://gist.github.com/hgbrian/affd44dc63c6fb01a5a9620c24c74b26) as suggested by [@design_proteins](https://x.com/design_proteins/status/1851308130392473919).
- Plotting helper function from [Stack Overflow](https://stackoverflow.com/a/50835066)

## Round 2 design strategies from other participants
- [Jude Wells](https://x.com/_judewells/status/1853805775807758465): [Chai1](https://doi.org/10.1101/2024.10.10.615955) + Adaptyv metrics + Rosetta InterfaceAnalyzer dG score
- keaun (via [OpenBioML Discord](https://www.openbioml.org/)): throwback method [PIPE](https://doi.org/10.1186/1471-2105-7-365)
- [@design_proteins](https://x.com/design_proteins/status/1854744521227092275): [Relaxed Sequence Optimization](https://doi.org/10.1126/science.adq1741) (RSO)
- [Team s1995825](https://x.com/leocastorina/status/1854640224359285006): [TIMED-Design](https://doi.org/10.1093/protein/gzae002)
- [@suzuki2001_](https://x.com/suzuki2001_/status/1854840776594993321) (aka begonia.sp.13): BindCraft and RSO + ColabFold + AlphaFold3 server, with details in a GitHub [repo](https://github.com/suzuki-2001/adaptyv-protein-comp)
- [cbrown](https://github.com/alpha29/BindCraft): BindCraft
- [antorsae](https://www.linkedin.com/pulse/our-jouney-adaptyvbio-protein-design-competition-bustos-md-phd-ykmaf): pipeline based on modifying endogenous ligands, includes [RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8)

## Apptainer build error
Errors encountered related to `/tmp` permissions during container build.
```
W: GPG error: https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease: Couldn't create temporary file /tmp/apt.conf.xCxAs0 for passing config to apt-key
E: The repository 'https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
W: GPG error: http://archive.ubuntu.com/ubuntu jammy InRelease: Couldn't create temporary file /tmp/apt.conf.Y4sBpz for passing config to apt-key
E: The repository 'http://archive.ubuntu.com/ubuntu jammy InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
W: GPG error: http://security.ubuntu.com/ubuntu jammy-security InRelease: Couldn't create temporary file /tmp/apt.conf.Yowfdp for passing config to apt-key
E: The repository 'http://security.ubuntu.com/ubuntu jammy-security InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
W: GPG error: http://archive.ubuntu.com/ubuntu jammy-updates InRelease: Couldn't create temporary file /tmp/apt.conf.UWUUTx for passing config to apt-key
E: The repository 'http://archive.ubuntu.com/ubuntu jammy-updates InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
W: GPG error: http://archive.ubuntu.com/ubuntu jammy-backports InRelease: Couldn't create temporary file /tmp/apt.conf.LZi0X8 for passing config to apt-key
E: The repository 'http://archive.ubuntu.com/ubuntu jammy-backports InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
+ apt install -y build-essential libgfortran5 git curl wget
```