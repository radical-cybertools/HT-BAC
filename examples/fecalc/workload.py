""" (Sample) workload definition file for .
"""

# ATTENTION:
# Read the tutorial instructions: 
#   https://github.com/radical-cybertools/HT-BAC/blob/master/README.md

WORKLOAD = []

for tj in range(0, 32):

    task = {
    	# Runtime of the MMPBSA task.
        "runtime" : 60,
        # Number of cores to use for the MMPBSA task.
        "cores"   : 1,
        # MMPBSA input file.
        "input"           : "./mmpbsa-sample-data/nmode.5h.py",
        # Complex topology file
        "complex_prmtop"  : "./mmpbsa-sample-data/com.top.2",
        # Receptor topology file
        "receptor_prmtop" : "./mmpbsa-sample-data/rec.top.2",
        # Ligand topology file.
        "ligand_prmtop"   : "./mmpbsa-sample-data/lig.top",
        # Input trajectories to analyze.
        "trajectory"      : "./mmpbsa-sample-data/trajectories/rep1.traj", 
        # Output filename.
        "output"  : "mmpbsa-task-%s.out" % tj
    }

    WORKLOAD.append(task)
