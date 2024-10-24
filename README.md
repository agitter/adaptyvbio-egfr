# Adaptyv EGFR protein design competition round 2

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
wget -O bindcraft-v1.1.0.zip https://github.com/martinpacesa/BindCraft/archive/refs/tags/v1.1.0.zip
```

## AlphaFold2 weights
The AlphaFold2 weights were downloaded and copied to [CHTC staging](https://chtc.cs.wisc.edu/uw-research-computing/file-avail-largedata.html)
```
curl -o params/alphafold_params_2022-12-06.tar https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
cd params/
$ scp alphafold_params_2022-12-06.tar agitter@transfer.chtc.wisc.edu:/staging/agitter/
```

## Third-party files
- `bindcraft.def`: Apptainer Definition file created by [@komatsuna-san](https://github.com/martinpacesa/BindCraft/issues/23#issuecomment-2408333526).
- `bindcraft-v1.1.0.zip`: BindCraft [v1.1.0 release](https://github.com/martinpacesa/BindCraft/releases/tag/v1.1.0) archive. Available under the [MIT License](https://github.com/martinpacesa/BindCraft/blob/main/LICENSE).
- `PDL1_example`: BindCraft example files in this subdirectory are from its [GitHub repo](https://github.com/martinpacesa/BindCraft/tree/d2d3cd0b5d6b02d12d24afa59e640717e36f552c) (version 1.1.0). Available under the [MIT License](https://github.com/martinpacesa/BindCraft/blob/main/LICENSE).

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