""" Application kernel configuration file.
"""

KERNEL = {

    "stampede.tacc.utexas.edu": 
    {
        "params": 
        {
            "cores_per_node": 16,
        },
        "kernel":
        {
            "mmpbsa": {
                "environment"   : {},
                "pre_execution" : "module load TACC && module load amber",
                "executable"    : "/opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/MMPBSA.py"
            },
            "namd": {
                "environment"   : {},
                "pre_execution" : "module load TACC && module load namd/2.9",
                "executable"    : "/opt/apps/intel13/mvapich2_1_9/namd/2.9/bin/namd2"
            }
        }
    }
}
