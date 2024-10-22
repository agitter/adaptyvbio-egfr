# Adaptyv EGFR protein design competition round 2

## Building BindCraft
Apptainer Definition file `bindcraft.def` created by [@komatsuna-san](https://github.com/martinpacesa/BindCraft/issues/23#issuecomment-2408333526).

I built the Apptainer container with an interactive CHTC job following their [instructions](https://chtc.cs.wisc.edu/uw-research-computing/apptainer-htc) and the submit file `build_bindcraft.sub`.
This was submitted with ` condor_submit -i build_bindcraft.sub`.

Within the interactive job, I ran
```
chmod 1777 /tmp
apptainer build bindcraft.sif bindcraft.def
mv bindcraft.sif /staging/agitter
```
`chmod` was needed to address errors related to [temporary files](https://superuser.com/questions/1496529/sudo-apt-get-update-couldnt-create-temporary-file) encountered during the container build.

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