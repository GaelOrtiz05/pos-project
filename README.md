Prerequisites (WINDOWS):
  Powershell 7 
  
  Python
  
  Git
  
  CMake

How to download prerequisites (WINDOWS):

Run these one by one in Admin Powershell to download them:
```
// Run this first to install latest version of Powershell 7
winget install -e --id Microsoft.PowerShell

// Then run these in Powershell 7
winget install -e --id Python.Python.3.14
winget install -e --id Git.Git
winget install -e --id Kitware.CMake
```

Make sure they are in installed and in your path:
```
python --version
git --version
cmake --version
```

How to download prerequisites (MACOS):

Prerequisites (MACOS): 

  Brew
  
  Python
  
  Git
  
  CMake

Brew is not necessary but it is a linux/macos package manager that makes installation much easier.

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
(NOTE) After the script installs, there will be a couple of lines of code under "Next Steps:"
Make sure you copy and paste those in the terminal.

Then Run:
```
brew update

brew install git cmake python@3.14
```

In a terminal run:
```
  git clone --recurse-submodules https://github.com/GaelOrtiz05/pos-project.git
  cd pos-project
```
Create a python virtual environment:
```
python -m venv venv
```
Activate virtual environment:
```
# Macos
source venv/bin/activate
# Windows
. .\venv\Scripts\activate
```
Install PySide6 (The GUI Library)
```
pip install PySide6
```
You will have to activate the virtual environment everytime you reopen the terminal to run it properly.

If you wish to exit the venv run `deactivate`

After you are sure you are in the venv, run:
```
mkdir build
cd build

# one line: requries you to be in build/
# Macos
cmake .. && make && python ../main.py

# Windows
cmake .. && cmake --build && python ../main.py
```
