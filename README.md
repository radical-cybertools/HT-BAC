# HT-BAC

HT-BAC provides a set of tools for molecular dynamics binding affinity calculations.

## 1. Installation

*Prerequisites*: Python >= 2.6, virtualenv >= 1.11 and pip >= 1.5.

The easiest way to install HT-BAC in user-space is to create 
a virtual environment:

```
virtualenv $HOME/HT-BAC-Tools
source $HOME/HT-BAC-Tools/bin/activate
```

The latest version of HT-BAC can be installed directly 
from GitHub:

```
pip install -e git://github.com/radical-cybertools/HT-BAC.git@release#egg=radical.ensemblemd.htbac
```

The following command should return the version number of the tools if the installation was successful:

```
python -c "import radical.ensemblemd.htbac; print radical.ensemblemd.htbac.version"
```

> If the above `pip install` or `python -c` command(s) fail, try to install HT-BAC from source:
> 
>    git clone https://github.com/radical-cybertools/HT-BAC.git -b release
>    cd HT-BAC
>    python setup.py install

# 2. Usage

## 2.1 Free Energy Calculations (`radical-bac-fecalc`)

This example shows how to run a set of free energy calculations using AMBER / [MMPBSA.py](http://pubs.acs.org/doi/abs/10.1021/ct300418h).

### 2.1.1 Configuration

A simple configuration file (`examples/fecalc/config.py`)is provided in which the allocation and resource 
parameters are set. Configuration files are passed to the `radical-freenerg-run` tool via the `--config=` flag. Change any of the values in the file to your specific needs: 

```
CONFIG = {
    "resource"      : "stampede.tacc.utexas.edu",
    "cores_per_node": 16,
    "username"      : "tg802352",
    "allocation"    : "TG-MCB090174"
}
```

### 2.1.2 Test Mode

The `radical-bac-fecalc` script provides two 'test modes' (`--checkenv` and `--testjob`) in which only a single task is submitted to the remote cluster to check wether the environment is healthy and usable.  

Before you start running large simulations on a resource, you should run `--checkenv` test mode at least once to ensure that the environment is ok:

```
$> radical-bac-fecalc --config=examples/fecalc/config.py --checkenv
``` 

The output should look like this:

```
 * Task 53331fa26bf88b22b2662eab state changed to 'PendingExecution'.
 * Resource '53331f9c6bf88b22b2662ea9' state changed to 'Running'.
 * Task 53331fa26bf88b22b2662eab state changed to 'Running'.
 * Task 53331fa26bf88b22b2662eab state changed to 'Done'.

RESULT:

MMPBSA path:/opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/MMPBSA.py
MMPBSA version:MMPBSA.py: Version 13.0
```

Once `--checkenv` has passed, you can run `--testjob`. In this test mode, a single free energy calculation job is launched together with some [sample input data](http://google.com) that is downloaded and transferred on the fly.  


```
$> radical-bac-fecalc --config=examples/bac/config.py --testjob
```

The output should look like this:

```
 * Task MMPBSA-fe-test-task state changed from 'New' to 'TransferringInput'.
 * Task MMPBSA-fe-test-task state changed from 'TransferringInput' to 'WaitingForExecution'.
 * Resource '<_BigJobWorker(_BigJobWorker-9, started daemon)>' state changed from 'New' to 'Pending'.
 * Task MMPBSA-fe-test-task state changed from 'WaitingForExecution' to 'Pending'.
 * Resource '<_BigJobWorker(_BigJobWorker-9, started daemon)>' state changed from 'Pending' to 'Running'.
 * Task MMPBSA-fe-test-task state changed from 'Pending' to 'Running'.
 * Task MMPBSA-fe-test-task state changed from 'Running' to 'WaitingForOutputTransfer'.
 * Task MMPBSA-fe-test-task state changed from 'WaitingForOutputTransfer' to 'TransferringOutput'.
 * Task MMPBSA-fe-test-task state changed from 'TransferringOutput' to 'Done'.

Test task results:
Loading and checking parameter files for compatibility...
Preparing trajectories for simulation...
20 frames were processed by cpptraj for use in calculation.

Running calculations on normal system...

Beginning GB calculations with /opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/mmpbsa_py_energy
  calculating complex contribution...
  calculating receptor contribution...
  calculating ligand contribution...

Beginning PB calculations with /opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/mmpbsa_py_energy
  calculating complex contribution...
  calculating receptor contribution...
  calculating ligand contribution...

Timing:
Total setup time:                           0.042 min.
Creating trajectories with cpptraj:         0.030 min.
Total calculation time:                     8.192 min.

Total GB calculation time:                  1.250 min.
Total PB calculation time:                  6.942 min.

Statistics calculation & output writing:    0.000 min.
Total time taken:                           8.274 min.


MMPBSA.py Finished! Thank you for using. Please cite us if you publish this work with this paper:
   Miller III, B. R., McGee Jr., T. D., Swails, J. M. Homeyer, N. Gohlke, H. and Roitberg, A. E.
   J. Chem. Theory Comput., 2012, 8 (9) pp 3314--3321
mmpbsa_py_energy found! Using /opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/mmpbsa_py_energy
cpptraj found! Using /opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/cpptraj
```

### 2.1.3 Running a Free Energy Calculation Workload

A sample workload file (`examples/bac/workload.py`) is provided in which multiple MMPBSA tasks are defined. A workload is passed to the radical-bac-fecalc.py tool via the --workload= flag. Change the workload in the file to your specific needs:

```
WORKLOAD = []

for tj in range(1, 2):

    task = {
        "runtime" : 60, # minutes per task
        "nmode"   : "/home1/00988/tg802352/MMPBSASampleDATA/nmode.5h.py",
        "com"     : "/home1/00988/tg802352/MMPBSASampleDATA/com.top.2",
        "rec"     : "/home1/00988/tg802352/MMPBSASampleDATA/rec.top.2",
        "lig"     : "/home1/00988/tg802352/MMPBSASampleDATA/lig.top",
        "traj"    : "/home1/00988/tg802352/MMPBSASampleDATA/trajectories/rep%s.traj" % tj,
    }

    WORKLOAD.append(task)
```

Once you have defined your workload you can execute it. Due to the potentially long runtime of your workload, it is highly advisable to run the script within a terminal multiplexer, like [tmux](http://robots.thoughtbot.com/a-tmux-crash-course). This allows you to _detach_ from your running script, log out from the lab machine and re-attach to it at a later point in time to check its progress.

> TIP: To start a new tmux session, type
> 
>     tmux
>    
> You can *detach* from a running tmux session by pressing `Ctrl-B D` and *re-attach* by launching tmux via `tmux attach`.

In your (new) `tmux` session, active your virtual environment and launch your workload:

```
source $HOME/MDStack/bin/activate

radical-bac-fecalc --config=config.py --workload=workload.py
```

Now you can detach from your tmux session or simply leave the terminal open. At some point you will see a message similar to this:

```
DONE -- All trajectories have been processed.
```

You will find the `FINAL_RESULTS_MMPBSA.dat` files for the individual tasks in the current directory. 




