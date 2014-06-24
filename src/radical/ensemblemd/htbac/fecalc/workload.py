#!/usr/bin/env python

"""This module implements radical-bac-fecalc --benchmark.
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import imp
import os, sys, uuid
import urllib
import optparse
import radical.pilot 

from radical.ensemblemd.mdkernels import MDTaskDescription
from radical.ensemblemd.htbac.common import BatchRunner

# ----------------------------------------------------------------------------
#
def run_workload(config, workload):
    # """Runs a workload.
    # """
    server     = config.SERVER
    dbname     = config.DBNAME
    maxcpus    = config.MAXCPUS
    resource   = config.RESOURCE
    username   = config.USERNAME
    allocation = config.ALLOCATION

    # We cannot allocate more than "maxcpus". If the number of tasks is 
    # smaller than 'maxcpus', we chose the closest increment of 16. If it
    # is larger, we use "maxcpus" and adjust the runtime of the pilot.

    # NOTE: currently, we assume (near) homogenous runtime among all tasks.
    task_runtime = workload[0]["runtime"]

    cores = 0
    for task in workload:
        cores += task["cores"]

    if cores < maxcpus:
        pilot_size = cores
        pilot_runtime = task_runtime
    else:
        pilot_size = maxcpus
        pilot_runtime = task_runtime * (len(workload)/maxcpus)
        if len(workload)%maxcpus > 0:
            pilot_runtime += task_runtime

    print "\n * Number of tasks: %s" % len(workload)
    print " * Pilot size (# cores): %s" % pilot_size
    print " * Pilot runtime: %s\n" % pilot_runtime

    ############################################################
    # The pilot description
    pdesc = radical.pilot.ComputePilotDescription()
    pdesc.resource   = resource
    pdesc.runtime    = pilot_runtime
    pdesc.cores      = pilot_size
    pdesc.project    = allocation
    pdesc.cleanup    = False



    ############################################################
    # Workload definition
    tasknum   = 0
    all_tasks = []

    # Create CU descriptions from workload taks...
    for task in workload:
        tasknum += 1

        # Process data handling.
        idl = task["input_data_location"]
        if idl.lower() == "local":
            idl_remote = False
        elif idl.lower() == "remote":
            idl_remote = True
        else:
            print "Unknown 'input_data_location': {0}".format(idl) 

        idl = task["output_data_location"]
        if idl.lower() == "local":
            odl_remote = False
        elif idl.lower() == "remote":
            odl_remote = True
        else:
            print "Unknown 'output_data_location': {0}".format(odl) 

        input_nmode = task["input"]
        nmode_basen = os.path.basename(input_nmode)

        input_com   = task["complex_prmtop"]
        com_basen   = os.path.basename(input_com)

        input_rec   = task["receptor_prmtop"]
        rec_basen   = os.path.basename(input_rec)

        input_lig   = task["ligand_prmtop"]
        lig_basen   = os.path.basename(input_lig)

        input_traj  = task["trajectory"]
        traj_basen  = os.path.basename(input_traj)

        output      = task["output"]

        mdtd = MDTaskDescription()
        mdtd.kernel = "MMPBSA"
        mdtd.arguments = "-i {0} -cp {1} -rp {2} -lp {3} -y {4}".format(nmode_basen, com_basen, rec_basen, lig_basen, traj_basen)

        if idl_remote is True:
            mdtd.copy_local_input_data = [input_nmode, input_com, input_rec, input_lig, input_traj]

        mdtd_bound = mdtd.bind(resource=resource)

        mmpbsa_task = radical.pilot.ComputeUnitDescription()
        mmpbsa_task.environment = mdtd_bound.environment 
        mmpbsa_task.pre_exec    = mdtd_bound.pre_exec
        mmpbsa_task.executable  = mdtd_bound.executable
        mmpbsa_task.arguments   = mdtd_bound.arguments
        mmpbsa_task.mpi         = mdtd_bound.mpi
        mmpbsa_task.cores       = task["cores"]
        mmpbsa_task.name        = task["name"]

        if idl_remote is False:
            # No remote files. All files are local and need to be transferred
            mmpbsa_task.input_data  = [input_nmode, input_com, input_rec, input_lig, input_traj]


        mmpbsa_task.output_data = ["FINAL_RESULTS_MMPBSA.dat > %s" % output]

        all_tasks.append(mmpbsa_task)

    ############################################################
    # Call the batch runner
    br = BatchRunner(config=config)
    finished_units = br.run(pilot_description=pdesc, cu_descriptions=all_tasks)
    if type(finished_units) != list:
        finished_units = [finished_units]

    print "\nDONE"
    print "=============================================================================\n"

    for unit in finished_units:
        t_start = unit.start_time
        t_stop = unit.stop_time
        t_run = t_stop - t_start

        local_output = unit.description.output_data[0].split(" > ")[1]
        print " o Task {0} RUNTIME {1} OUTPUT: {2}".format(unit.description.name, t_run, local_output)

    br.close()

