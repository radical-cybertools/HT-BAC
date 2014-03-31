""" User configuration file.
"""

#------------------------------------------------------------------------------
# Change the values below according to your requirements.
#
RESOURCE   = "stampede.tacc.utexas.edu"   # The name of the remote machine.
USERNAME   = "tg802352"                   # Your username on the remote machine.
ALLOCATION = "TG-MCB090174"               # The allocation or project to charge.
MAXCPUS    = 64                           # Maximum number of CPUs to allocate.

#------------------------------------------------------------------------------
# The settings below are only relevant if you want to run the benchmarks.
#
BENCHMARK_PILOT_SIZES  = [16, 32, 64, 128, 256, 512] # Pilot sizes to allocate. 
BENCHMARK_TASK_BATCHES = 4  # Number of tasks batches to run for each pilot 
                            # size. For example, for pilot size 16, a task
                            # batch '4' will submit 16, 32, 48 and 64 tasks.