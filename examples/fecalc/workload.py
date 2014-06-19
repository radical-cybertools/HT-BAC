""" (Sample) workload definition file for .
"""

# ATTENTION:
# Read the tutorial instructions: 
#   https://github.com/radical-cybertools/HT-BAC/blob/master/README.md

WORKLOAD = []

root_dir = "/Users/oweidner/htbac-examples/"

# We define 32 tasks -- for practical purposes, they are all the same.
for tj in range(0, 1):

    task = {
    	# Runtime of the MMPBSA task. With 4 cores, it takes roughly 10 minutes.
        "runtime" : 10,
        # Number of cores to use for the MMPBSA task (uses MPI)
        "cores"   : 4,
        # MMPBSA input file.
        "input"           : root_dir+"./mmpbsa-sample-data/nmode.5h.py",
        # Complex topology file
        "complex_prmtop"  : root_dir+"./mmpbsa-sample-data/com.top.2",
        # Receptor topology file
        "receptor_prmtop" : root_dir+"./mmpbsa-sample-data/rec.top.2",
        # Ligand topology file.
        "ligand_prmtop"   : root_dir+"./mmpbsa-sample-data/lig.top",
        # Input trajectories to analyze.
        "trajectory"      : root_dir+"./mmpbsa-sample-data/trajectories/rep1.traj", 
        # Output filename.
        "output"  : "mmpbsa-task-%s.out" % tj
    }

    WORKLOAD.append(task)
