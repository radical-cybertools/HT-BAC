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

from radical.ensemblemd.bac.common import run_testjob as testjob
from radical.ensemblemd.bac.callbacks import *
from radical.ensemblemd.bac.kernel import KERNEL


# ----------------------------------------------------------------------------
#
def run_testjob(config):
    """Runs a single FE test job.
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

    # --------------------------------------------------
    # Download the sample data from  server
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

    # --------------------------------------------------
    # The pilot description.
    pdesc = radical.pilot.ComputePilotDescription()
    pdesc.resource   = resource
    pdesc.runtime    = 15 # minutes
    pdesc.cores      = int(cores_per_node) * 1 # one node
    pdesc.project    = allocation
    pdesc.cleanup    = True

    # --------------------------------------------------
    # The test task description.
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

    # --------------------------------------------------
    # RUN THE TEST JOB VIA RADICAL-PILOT
    result = testjob(
        config=config,
        pilot_description=pdesc,
        cu_description=mmpbsa_test_task)

    # --------------------------------------------------
    # Try to remove the sample input data - silently fail on error.
    try:
        for key, val in sampledata.iteritems():
            os.remove("./%s" % key)
    except Exception:
        pass

    return result
