#!/usr/bin/env python

"""This module implements radical-bac-fecalc --benchmark. 
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import os
import sys
import imp
import uuid
import urllib
import optparse
import radical.pilot

from radical.ensemblemd.bac.callbacks import *
from radical.ensemblemd.bac.kernel import KERNEL


# -----------------------------------------------
#
def run_checkenv(config):
    """Runs a simple job that performs some sanity tests, determines
    AMBER version, etc.
    """
    server = config.SERVER
    dbname = config.DBNAME
    rconfs = config.RCONFS

    maxcpus = config.MAXCPUS
    resource = config.RESOURCE
    username = config.USERNAME
    allocation = config.ALLOCATION

    resource_params = KERNEL[resource]["params"]
    cores_per_node = resource_params["cores_per_node"]

    kernelcfg = KERNEL[resource]["kernel"]["mmpbsa"]

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

        pilot = pmgr.submit_pilots(pdesc)

        ############################################################
        # The checkenv task

        task_desc = radical.pilot.ComputeUnitDescription()
        task_desc.environment = kernelcfg["environment"]
        task_desc.executable = "/bin/bash"
        task_desc.arguments = ["-l", "-c", "\"%s && echo -n MMPBSA path: && which %s && echo -n MMPBSA version: && %s --version\"" % \
                (kernelcfg["pre_execution"], kernelcfg["executable"], kernelcfg["executable"]) ]
        task_desc.cores = 1

        umgr = radical.pilot.UnitManager(session=session,
            scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
        umgr.register_callback(task_cb)
        umgr.add_pilots(pilot)

        task = umgr.submit_units(task_desc)
        umgr.wait_units()

        print "\nRESULT:\n"
        print task.stdout

        session.close()

    except radical.pilot.PilotException, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    return 0