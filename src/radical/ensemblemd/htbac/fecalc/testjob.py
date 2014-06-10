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
from radical.ensemblemd.htbac.common import run_testjob as testjob


# ----------------------------------------------------------------------------
#
def run_testjob(config):
    """Runs a single FE test job.
    """
    resource = config.RESOURCE
    username = config.USERNAME
    allocation = config.ALLOCATION

    # --------------------------------------------------
    # Download the sample data from  server
    sampledata_base_url = config.SAMPLEDATA
    sampledata = {
        "nmode.5h.py" : "%s/BAC-MMBPSA/nmode.5h.py" % sampledata_base_url,
        "com.top.2"   : "%s/BAC-MMBPSA/com.top.2" % sampledata_base_url,
        "rec.top.2"   : "%s/BAC-MMBPSA/rec.top.2" % sampledata_base_url,
        "lig.top"     : "%s/BAC-MMBPSA/lig.top" % sampledata_base_url,
        "rep1.traj"   : "%s/BAC-MMBPSA/trajectories/rep1.traj" % sampledata_base_url
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
    pdesc.cores      = 4
    pdesc.project    = allocation
    pdesc.cleanup    = True

    # --------------------------------------------------
    # The test task description.

    mdtd = MDTaskDescription()
    mdtd.kernel = "MMPBSA"
    mdtd.arguments = "-i nmode.5h.py -cp com.top.2 -rp rec.top.2 -lp lig.top -y rep1.traj"

    mdtd_bound = mdtd.bind(resource=resource)

    mmpbsa_test_task = radical.pilot.ComputeUnitDescription()
    mmpbsa_test_task.environment = mdtd_bound.environment 
    mmpbsa_test_task.pre_exec    = mdtd_bound.pre_exec
    mmpbsa_test_task.executable  = mdtd_bound.executable
    mmpbsa_test_task.arguments   = mdtd_bound.arguments
    mmpbsa_test_task.mpi         = mdtd_bound.mpi
    mmpbsa_test_task.cores       = 4

    mmpbsa_test_task.input_data  = ["/%s/nmode.5h.py" % os.getcwd(),
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
