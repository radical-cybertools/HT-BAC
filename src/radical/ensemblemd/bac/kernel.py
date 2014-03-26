""" Application kernel configuration file.
"""

KERNEL = {

    "MMPBSA" : 
    {
        "description" : "MMPBSA is AMBER's free energy calculator.",
        "resources" : 
        { 
            "stampede.tacc.utexas.edu" : 
            {
                "environment"   : {"FOO": "BAR"},
                "pre_execution" : "module load amber",
                "executable"    : "/opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/MMPBSA.py"
            }
        }
    },

    'DUMMY' : 
    {
        "description" : "A dummy free energy calculator that does NOTHING.",
        "resources" : 
        { 
            "stampede.tacc.utexas.edu" : 
            {
                "pre_execution" : "/bin/true",
                "executable"    : "/bin/sleep 10"
            }
        }
    }
}
