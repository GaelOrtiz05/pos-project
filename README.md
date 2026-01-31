In a terminal run:
```
  git clone --recurse-submodules https://github.com/GaelOrtiz05/pos-project.git
  cd pos-project
```
Create a python virtual environment:
```
python3 -m venv venv
```
Activate virtual environment:
```
# Macos
source venv/bin/activate
# Windows
. \venv\Scripts\activate
```
Install PySide6 (The GUI Library)
```
pip install PySide6
```
You will have to activate the virtual environment everytime you reopen the terminal to run it properly.

After you are sure you are in the venv, run:
```
mkdir build
cd build
cmake ..
make
python ../main.py

# one line: requries you to be in build/
cmake .. && make && python3 ../main.py
```

