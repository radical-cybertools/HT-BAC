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


## 2. Usage Examples

### 2.1 Preparation 

*NOTE:* We will use TACC's [stampede](https://www.tacc.utexas.edu/stampede/) cluster
for these examples.

Before your run the examples, please create a new directory, e.g., in your `$HOME` directory
and copy our sample configuration files into it:

```
mkdir $HOME/htbac-examples
cd $HOME/htback-examples
wget wget https://raw.githubusercontent.com/radical-cybertools/HT-BAC/release/examples/config.py

```

Next, open `config.py` and change the following lines to match your stampede / TACC account:

```
USERNAME   = "your_username"               # Your username on the remote machine.
ALLOCATION = "your_allocation"             # The allocation or project to charge.
```

> If you don't have `wget` installed, you can just copy and paste the content of the  
> URL above into a file called `config.py`.

In order for HT-BAC to work, you also need password-less SSH-key access to 
the remote cluster. Tools like [ssh keychain](http://www.enterprisenetworkingplanet.com/netsecur/article.php/3469681/The-Practically-Ultimate-OpenSSHKeychain-Howto.htm) help with that. *Make sure you 
can SSH into the remote cluster without being asked for a passord before you proceed*.

### 2.2 Free Energy Calculations (`htbac-fecalc`)

In this example we run a set of 64 free energy calculations using AMBER / [MMPBSA.py](http://pubs.acs.org/doi/abs/10.1021/ct300418h). For demonstration purposes, the input data for all 32 tasks is identical, but this can obvisouly be changed easily.

#### Check the Enironment

Before you start running large simulations on a resource, you should run `htbac-fecalc --checkenv` at least once to ensure that the environment is ok:

```
htbac-fecalc --config=config.py --checkenv
``` 

The output should look like this:

```
 * Task 53690d7fb6158537540658cc state changed to 'PendingExecution'.
 * Resource '53690d77b6158537540658ca' state changed to 'Running'.
 * Task 53690d7fb6158537540658cc state changed to 'Running'.
 * Task 53690d7fb6158537540658cc state changed to 'Done'.

RESULT:

MMPBSA path:/opt/apps/intel13/mvapich2_1_9/amber/12.0/bin/MMPBSA.py
MMPBSA version:MMPBSA.py: Version 13.0

```

#### Run the Sample Workload

If `--checkenv` has passed, we can safely assume that the execution environment 
on the remote cluster is at least half-way decent and capable of executing 
MMPBSA tasks. 

Now we download the data for our sample workload:

```
wget http://testing.saga-project.org/cybertools/sampledata/BAC-MMBPSA/mmpbsa-sampledata.tar.gz
tar xzf mmpbsa-sampledata.tar.gz
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




