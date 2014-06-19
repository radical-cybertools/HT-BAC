""" (Sample) workload definition file for 'simchain'
"""

# ATTENTION:
# Read the tutorial instructions: 
#   https://github.com/radical-cybertools/HT-BAC/blob/master/README.md

WORKLOAD = []

root_dir = "/Users/oweidner/htbac-examples/"

# We define 16 tasks with 16 cores each -- for practical purposes, they are all the same.
for tj in range(0, 16):

    task = {
        "runtime"            : 30,
        "cores"              : 16,
        "parmfile"           : root_dir+"./simchain-sample-data/complex.top",
        "coordinates"        : root_dir+"./simchain-sample-data/complex.pdb",
        "conskfile"          : root_dir+"./simchain-sample-data/cons.pdb",
        "input"              : root_dir+"./simchain-sample-data/eq0.inp",
        "output"             : "simchain-task-%s.out" % tj
    }

    WORKLOAD.append(task)
