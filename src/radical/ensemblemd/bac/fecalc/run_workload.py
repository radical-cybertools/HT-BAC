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

    return 

    tasknum   = 0
    all_tasks = []

    for task in workload:
        print task

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
        pdesc.runtime    = 15 # minutes
        pdesc.cores      = int(cores_per_node) * 1 # one node
        pdesc.project    = allocation
        pdesc.cleanup    = True



        #pilot = pmgr.submit_pilots(pdesc)

        ############################################################
        # The workload
        tasknum   = 0
        all_tasks = []

        for task in workload:
            print task

        ############################################################
        # The test task
    #     output_file = "./MMPBSA-test-task-%s" % str(uuid.uuid4())

    #     mmpbsa_test_task = radical.pilot.ComputeUnitDescription()
    #     mmpbsa_test_task.environment = kernelcfg["environment"]
    #     mmpbsa_test_task.executable = "/bin/bash"
    #     mmpbsa_test_task.arguments   = ["-l", "-c", "\"%s && %s -i nmode.5h.py -cp com.top.2 -rp rec.top.2 -lp lig.top -y rep1.traj \"" % \
    #         (kernelcfg["pre_execution"], kernelcfg["executable"])]
    #     mmpbsa_test_task.cores = 1
    #     mmpbsa_test_task.input_data = ["/%s/nmode.5h.py" % os.getcwd(),
    #                                    "/%s/com.top.2" % os.getcwd(),
    #                                    "/%s/rec.top.2" % os.getcwd(),
    #                                    "/%s/lig.top" % os.getcwd(),
    #                                    "/%s/rep1.traj" % os.getcwd()]

    #     umgr = radical.pilot.UnitManager(session=session,
    #         scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
    #     umgr.register_callback(task_cb)
    #     umgr.add_pilots(pilot)

    #     task = umgr.submit_units(mmpbsa_test_task)
    #     umgr.wait_units()

    #     print "\nRESULT:\n"
    #     print task.stdout

    #     session.close()

    except radical.pilot.PilotException, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    except Exception, ex:
        print "ERROR: %s" % str(ex)
        return 1

    # try:
    # #     with open(output_file, 'r') as content_file:
    # #         content = content_file.read()
    # #         print content
    # #     os.remove(output_file)

    #     for key, val in sampledata.iteritems():
    #         os.remove("./%s" % key)

    # except Exception:
    #     pass

    # return 0
