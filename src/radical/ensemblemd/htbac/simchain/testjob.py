#!/usr/bin/env python

"""This module implements radical-bac-fecalc --benchmark.
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import os
import uuid
import urllib
import radical.pilot 

from radical.ensemblemd.mdkernels import MDTaskDescription
from radical.ensemblemd.htbac.common import BatchRunner


# -----------------------------------------------------------------------------
#
def run_testjob(config):
    """Runs a single FE test job.
    """
    resource = config.RESOURCE
    username = config.USERNAME
    allocation = config.ALLOCATION

    ############################################################
    # Download the sample data from server
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

    ############################################################
    # The pilot description.
    pdesc = radical.pilot.ComputePilotDescription()
    pdesc.resource   = resource
    pdesc.runtime    = 30 # minutes
    pdesc.cores      = 16
    pdesc.project    = allocation
    pdesc.cleanup    = True

    ############################################################
    # The test task description.

    mdtd = MDTaskDescription()
    mdtd.kernel = "NAMD"
    mdtd.arguments = ["./eq0.inp"]

    mdtd_bound = mdtd.bind(resource=resource)

    mmpbsa_test_task = radical.pilot.ComputeUnitDescription()
    mmpbsa_test_task.environment = mdtd_bound.environment 
    mmpbsa_test_task.pre_exec    = mdtd_bound.pre_exec
    mmpbsa_test_task.executable  = mdtd_bound.executable
    mmpbsa_test_task.arguments   = mdtd_bound.arguments
    mmpbsa_test_task.mpi         = mdtd_bound.mpi
    mmpbsa_test_task.cores       = 16

    mmpbsa_test_task.input_data  = [ "/%s/complex.pdb" % os.getcwd(),
                                     "/%s/complex.top" % os.getcwd(),
                                     "/%s/cons.pdb" % os.getcwd(),
                                     "/%s/eq0.inp" % os.getcwd() ]

    output_file = "./NAMD-test-task-%s" % str(uuid.uuid4())
    mmpbsa_test_task.output_data = ["STDOUT > %s" % output_file]

    ############################################################
    # Call the batch runner
    br = BatchRunner(config=config)
    finished_units = br.run(pilot_description=pdesc, cu_descriptions=mmpbsa_test_task)

    print "\nRESULT:\n"
    print finished_units.stdout

    br.close()

    ############################################################
    # Try to remove the sample input data - silently fail on error.
    try:
        for key, val in sampledata.iteritems():
            os.remove("./%s" % key)
    except Exception:
        pass
