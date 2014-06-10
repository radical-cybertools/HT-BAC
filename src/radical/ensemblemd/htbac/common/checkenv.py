#!/usr/bin/env python

"""This module implements --checkenv. 
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import os
import sys
import imp
import uuid
import radical.pilot

from radical.ensemblemd.htbac.callbacks import *
from radical.ensemblemd.htbac.kernel import KERNEL


# -----------------------------------------------------------------------------
#
def run_checkenv(config, pilot_description, cu_description):
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

        pmgr = radical.pilot.PilotManager(session=session)
        pmgr.register_callback(resource_cb)

        pilot = pmgr.submit_pilots(pilot_description)

        umgr = radical.pilot.UnitManager(session=session,
            scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
        umgr.register_callback(task_cb)
        umgr.add_pilots(pilot)

        task = umgr.submit_units(cu_description)
        umgr.wait_units()

        print "\nRESULT:\n"
        print task.stdout

        session.close()

    except radical.pilot.PilotException, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    return 0