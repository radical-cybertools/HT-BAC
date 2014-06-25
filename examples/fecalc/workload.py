""" (Sample) workload definition file for .
"""

# ATTENTION:
#
# Read the tutorial instructions: 
#   https://github.com/radical-cybertools/HT-BAC/blob/master/README.md
# 
# You can download the sample data from:
#   http://testing.saga-project.org/cybertools/sampledata/BAC-MMPBSA/mmpbsa-sample-data.tgz

WORKLOAD = []

#INPUT_DATA_ROOT_DIR  = "/Users/oweidner/htbac-examples/mmpbsa-sample-data/"
INPUT_DATA_ROOT_DIR = "/work/00988/tg802352/htbac-sampledata/mmpbsa-sample-data/"

# We define 16 tasks with 4 cores each -- for practical purposes, they are all the same.
for tj in range(0, 16):

    task = {

    	# Runtime of the MMPBSA task. With 4 cores, it takes roughly 10 minutes.
        "runtime"         : 30,
        # Number of cores to use for the MMPBSA task (uses MPI)
        "cores"           : 4,
        # Give the task a name
        "name"            : "sample-fecalc-task-{0}".format(tj),

        # Location of the input data: "LOCAL" means on this machine 
        # (input transfer required), "REMOTE" means on the remote machine.
        "input_data_location"  : "REMOTE", 
        # Location to put the output data: "LOCAL" means on this machine 
        # (output transfer required)| "REMOTE" means on the remote machine.
        "output_data_location" : "LOCAL",

        # NAMD-specific input files.
        #
        "input"           : INPUT_DATA_ROOT_DIR+"./nmode.5h.py",
        # Complex topology file
        "complex_prmtop"  : INPUT_DATA_ROOT_DIR+"./com.top.2",
        # Receptor topology file
        "receptor_prmtop" : INPUT_DATA_ROOT_DIR+"./rec.top.2",
        # Ligand topology file.
        "ligand_prmtop"   : INPUT_DATA_ROOT_DIR+"./lig.top",
        # Input trajectories to analyze.
        "trajectory"      : INPUT_DATA_ROOT_DIR+"./trajectories/rep1.traj", 
        # Output filename.
        "output"          : "sample-mmpbsa-task-%s.out" % tj
    }

    WORKLOAD.append(task)
