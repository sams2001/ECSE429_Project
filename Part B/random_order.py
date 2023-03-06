from behave.__main__ import main as behave_main
import random
import glob
import os

names = [os.path.basename(x) for x in glob.glob('./features/*') if x.endswith(".feature")]
random.shuffle(names)

for name in names:
    print("Executing: {}".format(name))
    behave_main(["features/" + name])
