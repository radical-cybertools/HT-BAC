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
def run_testjob(config):
    # """Runs a single FE test job.
    # """

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

    # Download the sample data from MDStack server
    sampledata_base_url = config.SAMPLEDATA
    sampledata = {
        "nmode.5h.py" : "%s/MMBPSA/nmode.5h.py" % sampledata_base_url,
        "com.top.2"   : "%s/MMBPSA/com.top.2" % sampledata_base_url,
        "rec.top.2"   : "%s/MMBPSA/rec.top.2" % sampledata_base_url,
        "lig.top"     : "%s/MMBPSA/lig.top" % sampledata_base_url,
        "rep1.traj"   : "%s/MMBPSA/trajectories/rep1.traj" % sampledata_base_url
    }

    try:
        for key, val in sampledata.iteritems():
            print " * Downloading sample input data %s" % val
            urllib.urlretrieve(val, key)
    except Exception, ex:
        print "ERROR - Couldn't download sample data: %s" % str(ex)
        return 1

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
        # The test task
        output_file = "./MMPBSA-test-task-%s" % str(uuid.uuid4())

        mmpbsa_test_task = radical.pilot.ComputeUnitDescription()
        mmpbsa_test_task.environment = kernelcfg["environment"]
        mmpbsa_test_task.executable = "/bin/bash"
        mmpbsa_test_task.arguments   = ["-l", "-c", "\"%s && %s -i nmode.5h.py -cp com.top.2 -rp rec.top.2 -lp lig.top -y rep1.traj \"" % \
            (kernelcfg["pre_execution"], kernelcfg["executable"])]
        mmpbsa_test_task.cores = 1
        mmpbsa_test_task.input_data = ["/%s/nmode.5h.py" % os.getcwd(),
                                       "/%s/com.top.2" % os.getcwd(),
                                       "/%s/rec.top.2" % os.getcwd(),
                                       "/%s/lig.top" % os.getcwd(),
                                       "/%s/rep1.traj" % os.getcwd()]

        umgr = radical.pilot.UnitManager(session=session,
            scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
        umgr.register_callback(task_cb)
        umgr.add_pilots(pilot)

        task = umgr.submit_units(mmpbsa_test_task)
        umgr.wait_units()

        print "\nRESULT:\n"
        print task.stdout

        session.close()

    except radical.pilot.PilotException, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    try:
    #     with open(output_file, 'r') as content_file:
    #         content = content_file.read()
    #         print content
    #     os.remove(output_file)

        for key, val in sampledata.iteritems():
            os.remove("./%s" % key)

    except Exception:
        pass

    return 0
