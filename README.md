# HT-BAC Tools

HT-BAC provides a set of tools for running large number of parallel molecular dynamics binding affinity calculations on HPC clusters. It provides two command line tools:

* `htbac-simchain` - runs namd2 simulations (**see section 2.2**).
* `htbac-fecalc` - runs mmpbsa free energy calculations (**see section 2.3**).

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
pip install --upgrade git+https://github.com/radical-cybertools/radical.ensemblemd.mdkernels.git@release#egg=radical.ensemblemd.mdkernels
pip install --upgrade git+https://github.com/radical-cybertools/HT-BAC.git@release#egg=radical.ensemblemd.htbac
```

> If the above command doesn't work, you can check out the repository manually and install HT-BAC from source:
> 
> ```
>     git clone https://github.com/radical-cybertools/HT-BAC.git -b release HT-BAC-src
>     cd HT-BAC-src
>     pip install .
> ```

The following command should return the version number of the tools if the installation was successful:

```
python -c "import radical.ensemblemd.htbac; print radical.ensemblemd.htbac.version"
```


## 2. Usage Examples

### 2.1 Preparation 

**NOTE:** We will use TACC's [stampede](https://www.tacc.utexas.edu/stampede/) cluster
to run the example jobs. Since the HT-BAC tools can submit computational tasks to
a remote machine, all steps in this example should be done on a 'local' resource, e.g.,
your laptop. It is not neccessary to log in to stampede. 

Before your run the examples, please create a new directory, e.g., in your `$HOME` directory
and copy our sample configuration files into it:

```
mkdir $HOME/htbac-examples
cd $HOME/htbac-examples
wget --no-check-certificate https://raw.githubusercontent.com/radical-cybertools/HT-BAC/release/examples/config.py

```

Next, open `config.py` and change the following lines to match your stampede / TACC account:

```
USERNAME   = "your_username"               # Your username on the remote machine.
ALLOCATION = "your_allocation"             # The allocation or project to charge.
```

> If you don't have `wget` installed, you can just copy and paste the content of the  
> URL above into a file called `config.py`.

In order for HT-BAC to work, you also need password-less SSH-key access to 
the remote cluster. Tools like [ssh keychain](http://www.enterprisenetworkingplanet.com/netsecur/article.php/3469681/The-Practically-Ultimate-OpenSSHKeychain-Howto.htm) can help with that. *Make sure you 
can SSH into the remote cluster without being asked for a passord before you proceed*.

### 2.2 Free Energy Calculations (`htbac-fecalc`)

In this example we run a set of 16 free energy calculations using AMBER / [MMPBSA.py](http://pubs.acs.org/doi/abs/10.1021/ct300418h). For demonstration purposes, the input data for all 16 tasks is identical, but this can obvisouly be changed easily.

#### Check the Environment

Before you start running large simulations on a resource, you should run `htbac-fecalc --checkenv` at least once to ensure that the environment is ok:

> To see some additional information about task execution, you can set
> the environment variable `RADICAL_PILOT_VERBOSE=info`.

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

#### Define and Run the Sample Workload

If `--checkenv` has passed, we assume that the execution environment 
on the remote cluster is capable of executing MMPBSA tasks. 

Next, download the input data for the sample workload:

```
curl -O http://testing.saga-project.org/cybertools/sampledata/BAC-MMBPSA/mmpbsa-sample-data.tgz
tar xzf mmpbsa-sample-data.tgz
```

Next, define the workload (here we use the same input files for all tasks for simplicity).
Open a file `workload.py` and put in the following:

```
WORKLOAD = []

for tj in range(0, 16):

    task = {
        # Runtime of a 4-core MMPBSA task.
        "runtime"         : 5,
        # Number of cores to use for the MMPBSA task.
        "cores"           : 4,
        # Give the task a name
        "name"            : "sample-mmpbsa-task-{0}".format(tj),
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
        "output"          : "sample-mmpbsa-task-{0}.out".format(tj)
    }

    WORKLOAD.append(task)
```

> *Note:* HT-BAC workload files are Python scripts. This means that 
> you can define arbitrarily complex workload descriptions, as long
> as all tasks are appened to the global `WORKLOAD` list.

Now you are ready to run the workload with the `htbac-fecalc` tool:

```
htbac-fecalc --config=config.py --workload=workload.py
```

The workload will allocate `4*16` = **64 cores** and will take about *5 minutes* to execute. The output should look like this:

```
 * Number of tasks: 16
 * Pilot size (# cores): 64
 * Pilot runtime: 60

 * Task 53692e00b61585411691fb98 state changed to 'WaitingForInputTransfer'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForInputTransfer'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'TranferringInput'.
 * Task 53692e00b61585411691fb99 state changed to 'TranferringInput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'TranferringInput'.
 * Task 53692e00b61585411691fb99 state changed to 'TranferringInput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'WaitingForExecution'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForExecution'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'Executing'.
 * Task 53692e00b61585411691fb99 state changed to 'Executing'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'WaitingForOutputTransfer'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForOutputTransfer'.
  [...]
 * Task 53692e00b61585411691fb98 state changed to 'TransferringOutput'.
 * Task 53692e00b61585411691fb99 state changed to 'TransferringOutput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'Done'.
 * Task 53692e00b61585411691fb99 state changed to 'Done'.

 * Task 53692e00b61585411691fb98: state: Done, started: 2014-05-09 18:17:19.333000, finished: 2014-05-09 18:26:36.553000, results: mmpbsa-task-0.out
 * Task 53692e00b61585411691fb99: state: Done, started: 2014-05-09 18:17:20.385000, finished: 2014-05-09 18:26:32.193000, results: mmpbsa-task-1.out
 
DONE
=============================

 o Task sample-fecalc-task-0 (runtime 0:02:17.002000) output in: sample-mmpbsa-task-0.out
 o Task sample-fecalc-task-1 (runtime 0:02:17.748000) output in: sample-mmpbsa-task-1.out
 [...]

```

### 2.3 NAMD Simulation (`htbac-simchain`)

In this example we run a set of 16 free energy calculations using NAMD. For demonstration purposes, the input data for all 16 tasks is identical, but this can obvisouly be changed easily.

#### Check the Environment

Before you start running large simulations on a resource, you should run `htbac-simchain --checkenv` at least once to ensure that the environment is ok:

> To see some additional information about task execution, you can set
> the environment variable `RADICAL_PILOT_VERBOSE=info`. This can be useful to track down errors.

```
htbac-simchain --config=config.py --checkenv
``` 

The output should look like this:

```
 * Task 53690d7fb6158537540658cc state changed to 'PendingExecution'.
 * Resource '53690d77b6158537540658ca' state changed to 'Running'.
 * Task 53690d7fb6158537540658cc state changed to 'Running'.
 * Task 53690d7fb6158537540658cc state changed to 'Done'.

RESULT:

Info: NAMD 2.9 for Linux-x86_64-MPI
Info: 
Info: Please visit http://www.ks.uiuc.edu/Research/namd/
Info: for updates, documentation, and support information.
Info: 
Info: Please cite Phillips et al., J. Comp. Chem. 26:1781-1802 (2005)
Info: in all publications reporting results obtained with NAMD.
Info: 
Info: Based on Charm++/Converse 60400 for mpi-linux-x86_64
Info: Built Thu Jan 3 10:11:57 CST 2013 by root on build.stampede.tacc.utexas.edu
Info: 1 NAMD  2.9  Linux-x86_64-MPI  1    c406-302.stampede.tacc.utexas.edu  tg802352
Info: Running on 1 processors, 1 nodes, 1 physical nodes.
Info: CPU topology information available.
Info: Charm++/Converse parallel runtime startup completed at 0.00828314 s
```

> Due to some NAMD-internal issues, the task will show as `Failed`, however, 
> as long as the output is there, everything is ok.

#### Define and Run the Sample Workload

If `--checkenv` has passed, we assume that the execution environment 
on the remote cluster is capable of executing MMPBSA tasks. 

Next, download the input data for the sample workload:

```
curl -O http://testing.saga-project.org/cybertools/sampledata/BAC-SIMCHAIN/simchain-sample-data.tgz
tar xzf simchain-sample-data.tgz
```

Next, define the workload (here we use the same input files for all tasks for simplicity).
Open a file `workload.py` and put in the following:

```
WORKLOAD = []

for tj in range(0, 16):

    task = {
        "runtime"            : 15,
        "cores"              : 16,
        "parmfile"           : "./simchain-sample-data/complex.top",
        "coordinates"        : "./simchain-sample-data/complex.pdb",
        "conskfile"          : "./simchain-sample-data/cons.pdb",
        "input"              : "./simchain-sample-data/eq0.inp",
        "name"               : "sample-simchain-task-{0}".format(tj),
        "output"             : "sample-simchain-task-%s.out" % tj
    }

    WORKLOAD.append(task)
```

> *Note:* HT-BAC workload files are Python scripts. This means that 
> you can define arbitrarily complex workload descriptions, as long
> as all tasks are appened to the global `WORKLOAD` list.

Now you can run the workload with the `htbac-simchain` tool:

```
htbac-simchain --config=config.py --workload=workload.py
```

The workload will allocate `16*16` = **256 cores** and will take about *15 minutes* to execute. The output should look like this:

```
 * Number of tasks: 16
 * Pilot size (# cores): 256
 * Pilot runtime: 60

 * Task 53692e00b61585411691fb98 state changed to 'WaitingForInputTransfer'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForInputTransfer'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'TranferringInput'.
 * Task 53692e00b61585411691fb99 state changed to 'TranferringInput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'TranferringInput'.
 * Task 53692e00b61585411691fb99 state changed to 'TranferringInput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'WaitingForExecution'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForExecution'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'Executing'.
 * Task 53692e00b61585411691fb99 state changed to 'Executing'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'WaitingForOutputTransfer'.
 * Task 53692e00b61585411691fb99 state changed to 'WaitingForOutputTransfer'.
  [...]
 * Task 53692e00b61585411691fb98 state changed to 'TransferringOutput'.
 * Task 53692e00b61585411691fb99 state changed to 'TransferringOutput'.
 [...]
 * Task 53692e00b61585411691fb98 state changed to 'Done'.
 * Task 53692e00b61585411691fb99 state changed to 'Done'.

 * Task 53692e00b61585411691fb98: state: Done, started: 2014-05-09 18:17:19.333000, finished: 2014-05-09 18:26:36.553000, results: mmpbsa-task-0.out
 * Task 53692e00b61585411691fb99: state: Done, started: 2014-05-09 18:17:20.385000, finished: 2014-05-09 18:26:32.193000, results: mmpbsa-task-1.out
 
 DONE
=============================================================================

 o Task sample-simchain-task-0 RUNTIME 0:10:55.839000 OUTPUT: sample-simchain-task-0.out
 o Task sample-simchain-task-1 RUNTIME 0:10:53.536000 OUTPUT: sample-simchain-task-1.out
 [...]
 
 ```


## 3. Tips and Best Practice

### Use tmux for Long Running Simulations

Usually workloads take much longer to execute then the examples above. Some workloads 
can run for hours or even for days. Hence, it is highly advisable to run the script within a terminal multiplexer, like [tmux](http://robots.thoughtbot.com/a-tmux-crash-course). This allows you to _detach_ from your running script, log out from the lab machine and re-attach to it at a later point in time to check its progress.

To start a new tmux session, type
``` 
    tmux
```

You can *detach* from a running tmux session by pressing `Ctrl-B D` and *re-attach* by launching tmux via `tmux attach`.

In your (new) `tmux` session, active your virtual environment and launch your workload:

```
source $HOME/HT-BAC-Tools/bin/activate

htbac-fecalc --config=config.py --workload=workload.py
```

Now you can detach from your tmux session and even log out if you are connected via ssh. Later you 
can login and / or re-connect to your session again to check the progress of your simulations.



