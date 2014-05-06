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

from radical.ensemblemd.bac.callbacks import *
from radical.ensemblemd.bac.kernel import KERNEL


# ----------------------------------------------------------------------------
#
def run_workload(config, workload):
    # """Runs a workload.
    # """
    server = config.SERVER
    dbname = config.DBNAME
    rconfs = config.RCONFS

    maxcpus = config.MAXCPUS

    maxcpus = config.MAXCPUS
    resource = config.RESOURCE
    username = config.USERNAME
    allocation = config.ALLOCATION

    resource_params = KERNEL[resource]["params"]
    cores_per_node = resource_params["cores_per_node"]

    kernelcfg = KERNEL[resource]["kernel"]["mmpbsa"]

    # We cannot allocate more than "maxcpus". If the number of tasks is 
    # smaller than 'maxcpus', we chose the closest increment of 16. If it
    # is larger, we use "maxcpus" and adjust the runtime of the pilot.

    # NOTE: currently, we assume (near) homogenous runtime among all tasks.
    task_runtime = workload[0]["runtime"]

    if len(workload) < maxcpus:
        pilot_size = 16 * (len(workload) / 16)
        if len(workload) % 16 > 0:
            pilot_size += 16
        pilot_runtime = task_runtime
    else:
        pilot_size = maxcpus
        pilot_runtime = task_runtime * (len(workload)/maxcpus)
        if len(workload)%maxcpus > 0:
            pilot_runtime += task_runtime

    print "\n * Number of tasks: %s" % len(workload)
    print " * Pilot size (# cores): %s" % pilot_size
    print " * Pilot runtime: %s\n" % pilot_runtime

    tasknum   = 0
    all_tasks = []

    # Create CU descriptions from workload taks...
    for task in workload:
        tasknum += 1

        input_nmode = task["nmode"]
        input_com   = task["com"]
        input_rec   = task["rec"]
        input_lig   = task["lig"]
        input_traj  = task["traj"]

        mmpbsa_task = radical.pilot.ComputeUnitDescription()
        mmpbsa_task.environment = kernelcfg["environment"]
        mmpbsa_task.executable = "/bin/bash"
        mmpbsa_task.arguments = ["-l", "-c", "\"%s && %s -i %s -cp %s -rp %s -lp %s -y %s \"" % \
           (kernelcfg["pre_execution"], 
            kernelcfg["executable"], 
            input_nmode, input_com, input_rec, input_lig, input_traj
            )]

        mmpbsa_task.cores = 1
        mmpbsa_task.output_data = ["FINAL_RESULTS_MMPBSA.dat > traj-%s-FINAL_RESULTS_MMPBSA.dat" % tasknum]

        all_tasks.append(mmpbsa_task)

    # Now that we have created the CU descriptions, we can launch the 
    # pilot and submit the CUs. 
    session = radical.pilot.Session(database_url=server, database_name=dbname)

    try:
        # Add an ssh identity to the session.
        cred = radical.pilot.SSHCredential()
        cred.user_id = username
        session.add_credential(cred)

        ############################################################
        # The resource allocation
        pmgr = radical.pilot.PilotManager(
            session=session, resource_configurations=rconfs)
        pmgr.register_callback(resource_cb)

        pdesc = radical.pilot.ComputePilotDescription()
        pdesc.resource   = resource
        pdesc.runtime    = pilot_runtime
        pdesc.cores      = pilot_size
        pdesc.project    = allocation
        pdesc.cleanup    = True

        pilot = pmgr.submit_pilots(pdesc)
        pilot.register_callback(resource_cb)

        umgr = radical.pilot.UnitManager(session=session,
            scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
        umgr.register_callback(task_cb)
        umgr.add_pilots(pilot)

        tasks = umgr.submit_units(all_tasks)
        umgr.wait_units()

        print "\nRESULTS:"

        for task in tasks:
            print " * State: %s STDOUT: %s STDERR: %s" % (task.state, task.stdout, task.stderr)

        session.close()

    except radical.pilot.PilotException, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    except Exception, ex:
        print "ERROR: %s" % str(ex)
        return 1
