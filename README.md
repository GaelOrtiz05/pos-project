# How To Run (WINDOWS):

- Powershell 7
- Git
- Mise

How to download prerequisites (WINDOWS):

Run these one by one in an Admin Powershell to download them:

```bash
// Run this first to install latest version of Powershell 7
winget install -e --id Microsoft.PowerShell

// Then run these in Powershell 7 (Adminstrator Mode)
winget install -e --id Git.Git
winget install -e --id Kitware.CMake
winget install jdx.mise
```

Make sure they are in installed and in your path:

```bash
git --version
cmake --version
```

In powershell admin, run:

```bash
if (-not (Test-Path $profile)) { New-Item $profile -Force }
notepad $profile
```

This creates a profile if one doesn't exist already, and opens the profile to edit it.

Paste this in the profile:

```bash
if (Get-Command mise -ErrorAction SilentlyContinue) {
    mise activate pwsh | Invoke-Expression
}
```

run `mise reshim` first.
Then, Press Windows + r, type `sysdm.cpl`, go to the advanced tab, then environment variables.
Make sure `C:\Users\USER\AppData\Local\mise\shims` is at the top, if there are multiple, delete them and only keep one,
If this doesn't exist, add the path manually.

restart powershell one last time, and you should be good.

# How To Run (MACOS):

- Brew
- Mise

Brew is not necessary but it is a linux/macos package manager that makes installation much easier.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

> [!NOTE]
> After the script installs, there will be a couple of lines of code under "Next Steps:"
> Make sure you copy and paste those in the terminal.

Then Run:

```bash
brew update

brew install cmake git mise
```

depending on if you use bash or zsh, run either:

```bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
```

This is same as running something like `python -m venv venv`, but mise creates it automatically and uses them depending on your current directory.
You don't have to worry about running `source venv/bin/activate` or the equivalent for windows with mise.

In a terminal run:

```bash
  git clone --recurse-submodules https://github.com/GaelOrtiz05/pos-project.git
  cd pos-project
```

Then Run

```bash
mise install
mise run requirements
```

Run on windows:

```bash
mise run build_windows
```

Run on macos:

```bash
mise run build_macos
```
