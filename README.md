# Prerequisites:

- Git
- CMake
- Powershell 7 (Windows)

> [!NOTE]
> There are two ways to run this code, either manually or with mise. If you get through the initial insatllation of mise,
> not too hard, it will make running the code much easier.

# How To Run (WINDOWS):

Run these one by one in an Admin Powershell to download them:

## Installing Prerequisites

Run these in an administrator Powershell:

```bash
winget install -e --id Microsoft.PowerShell
winget install -e --id Git.Git
winget install -e --id Kitware.CMake
```

> [!NOTE]
> Restart your powershell to add them to your path and verify installation with:

```bash
git --version
cmake --version
```

## Setting up Mise

If you don't want to setup mise, skip this step.
In Powershell, run:

```bash
winget install jdx.mise

```

then:

```bash

if (-not (Test-Path $profile)) { New-Item $profile -Force }
echo '(&mise activate pwsh) | Out-String | Invoke-Expression' >> $PROFILE
notepad $profile
```

This creates a profile if one doesn't exist already, and opens the profile to edit it.
Make sure the profile looks like:

```bash
    mise activate pwsh | Invoke-Expression
```

> [!NOTE]
> Restart powershell one last time to apply the profile changes

# How To Run (MACOS):

## Installing Prerequisites

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
brew install cmake git
```

## Setting up Mise (MacOS)

If you don't want to setup mise, skip this step

```bash
brew install mise
```

Depending on if you use bash or zsh, run either:

```bash
# bash
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
# zsh
echo 'eval "$(mise activate zsh)"' >> ~/.zshrc
```

# Building

In a terminal run:

```bash
  git clone --recurse-submodules https://github.com/GaelOrtiz05/pos-project.git
  cd pos-project
```

> [!NOTE]
> run `git submodule update --init --recursive` if pybind11 is not under libraries

## Manually

Create a venv:

```bash
python -m venv venv
```

Activate it:

```bash
# Macos
source venv/bin/activate
# Windows
. .\venv\Scripts\activate
```

Install requirements

```bash
pip install -r requirements.txt
```

You will have to activate the virtual environment everytime you reopen the terminal to run it properly.

If you wish to exit the venv run deactivate

After you are sure you are in the venv, run:

```bash
mkdir build

# One line: requires you to be in project root
# Macos
cmake -S . -B build && cmake --build build && python3 src/python/main.py

# Windows
cmake -S . -B build && cmake --build build --config Debug && python src/python/main.py
```

## Mise

This is same as running something like `python -m venv venv`, but mise creates it automatically and uses them depending on your current directory.
You don't have to worry about running `source venv/bin/activate` or the equivalent for windows with mise.

You can create specific tasks in mise.toml and you can run them with `mise run`. This make building much cleaner

Run:

```bash
mise install
# Macro for pip install -r requirements.txt
mise run requirements
```

Run on windows:

```bash
# Macro for cmake -S . -B build && cmake --build build --config Debug && python src/python/main.py
mise run build_windows
```

Run on macos:

```bash
# Macro for cmake -S . -B build && cmake --build build && python3 src/python/main.py
mise run build_macos
```
