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

from radical.ensemblemd.htbac.common import run_testjob as testjob
from radical.ensemblemd.htbac.callbacks import *
from radical.ensemblemd.htbac.kernel import KERNEL


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
    kernelcfg = KERNEL[resource]["kernel"]["namd"]

    # --------------------------------------------------
    # Download the sample data from  server
    sampledata_base_url = config.SAMPLEDATA
    sampledata = {
        "complex.pdb" : "%s/BAC-SIM/complex.pdb" % sampledata_base_url,
        "complex.top" : "%s/BAC-SIM/complex.top" % sampledata_base_url,
        "cons.pdb"    : "%s/BAC-SIM/cons.pdb" % sampledata_base_url,
        "eq0.inp"     : "%s/BAC-SIM/eq0.inp" % sampledata_base_url,
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
    pdesc.runtime    = 30 # minutes
    pdesc.cores      = int(cores_per_node) * 1 # one node
    pdesc.project    = allocation
    pdesc.cleanup    = False

    # --------------------------------------------------
    # The test task description.
    output_file = "./NAMD-test-task-%s" % str(uuid.uuid4())

    mmpbsa_test_task = radical.pilot.ComputeUnitDescription()
    mmpbsa_test_task.environment = kernelcfg["environment"]
    mmpbsa_test_task.executable = "/bin/bash"
    mmpbsa_test_task.arguments   = ["-l", "-c", "\"module load namd/2.9 && namd2 ./eq0.inp \""]
    mmpbsa_test_task.cores = 1
    mmpbsa_test_task.input_data = ["/%s/complex.pdb" % os.getcwd(),
                                   "/%s/complex.top" % os.getcwd(),
                                   "/%s/cons.pdb" % os.getcwd(),
                                   "/%s/eq0.inp" % os.getcwd()]
    mmpbsa_test_task.output_data = ["STDOUT > %s" % output_file]

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
