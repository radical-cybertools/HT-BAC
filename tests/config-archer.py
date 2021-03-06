""" User configuration file.
"""

#------------------------------------------------------------------------------
# Change the values below according to your requirements.
#
RESOURCE   = "archer.ac.uk"                # The name of the remote machine.
USERNAME   = "ocwe10"                      # Your username on the remote machine.
ALLOCATION = "e10-ocwe10"                  # The allocation or project to charge.
WORKDIR    = "/work/e10/e10/ocwe10/HT-BAC" # The working directory ("sandbox")
MAXCPUS    = 1024                          # Maximum number of CPUs to allocate.

#------------------------------------------------------------------------------
# Change the settings below *ONLY* if you want to use a different MongoDB
# server or different / additional resource configuration files.
#
SERVER     = "mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017"
DBNAME     = "radical-ensemblemd"

#------------------------------------------------------------------------------
# SAMPLEDATA points to the sample data location that is used for the
# --testjob modes. DON'T CHANGE THIS.
#
SAMPLEDATA = "http://testing.saga-project.org/cybertools/sampledata/"

#------------------------------------------------------------------------------
# The settings below are only relevant if you want to run the benchmarks.
#
INPUT_DATA_ROOT_DIR = "/work/00988/tg802352/htbac-sampledata/mmpbsa-sample-data/"

FECALC_BENCHMARK_DBNAME              = "radical-ensemblemd-htbac-fecalc-benchmark"
FECALC_BENCHMARK_PILOT_SIZES         = [16, 32, 64, 128, 256, 512, 1024]
FECALC_BENCHMARK_TASK_PARALLELISM    = [1]
FECALC_BENCHMARK_INPUT_DATA_LOCATION = "REMOTE"
FECALC_BENCHMARK_INPUT_DATA          = [INPUT_DATA_ROOT_DIR+"./nmode.5h.py",
                                        INPUT_DATA_ROOT_DIR+"./com.top.2",
                                        INPUT_DATA_ROOT_DIR+"./rec.top.2",
                                        INPUT_DATA_ROOT_DIR+"./lig.top",
                                        INPUT_DATA_ROOT_DIR+"./trajectories/rep1.traj"]