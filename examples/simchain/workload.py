""" (Sample) workload definition file for 'simchain'
"""

# ATTENTION:
#
# Read the tutorial instructions: 
#   https://github.com/radical-cybertools/HT-BAC/blob/master/README.md
# 
# You can download the sample data from:
#   http://testing.saga-project.org/cybertools/sampledata/BAC-SIMCHAIN/simchain-sample-data.tgz

WORKLOAD = []

INPUT_DATA_ROOT_DIR  = "/Users/oweidner/htbac-examples/simchain-sample-data/"
#INPUT_DATA_ROOT_DIR = "/home1/00988/tg802352/htbac-sampledata/simchain-sample-data/"

# We define 16 tasks with 16 cores each -- for practical purposes, they are all the same.
for tj in range(0, 16):

    task = {

        # Task properties.
        # 
        "runtime"              : 30,
        "cores"                : 16,
        "name"                 : "sample-simchain-task-{0}".format(tj),

        # Location of the input data: "LOCAL" means on this machine 
        # (input transfer required), "REMOTE" means on the remote machine.
        "input_data_location"  : "LOCAL", 
        # Location to put the output data: "LOCAL" means on this machine 
        # (output transfer required)| "REMOTE" means on the remote machine.
        "output_data_location" : "LOCAL",

        # NAMD-specific input files.
        #
        "parmfile"             : INPUT_DATA_ROOT_DIR+"./complex.top",
        "coordinates"          : INPUT_DATA_ROOT_DIR+"./complex.pdb",
        "conskfile"            : INPUT_DATA_ROOT_DIR+"./cons.pdb",
        "input"                : INPUT_DATA_ROOT_DIR+"./eq0.inp",
        "output"               : "sample-simchain-task-%s.out" % tj
    }

    WORKLOAD.append(task)
