import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, "build"))

import backend

# use the module name as a prefix to the class
pos = backend.POS()

pos.addItem("Apple", 1.50)
print(f"Total with tax: {pos.getTotal()}")
