#!/usr/bin/env python

"""This tool runs free energy calculations with Amber MMPBSA.py. 
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import imp
import os, sys, uuid
import optparse

#from radical.ensemblemd.htbac.sim import run_benchmark
#from radical.ensemblemd.htbac.sim import run_workload
from radical.ensemblemd.htbac.sim import run_checkenv
from radical.ensemblemd.htbac.sim import run_testjob


# ----------------------------------------------------------------------------
#
def main():

    usage = "usage: %prog --config [--checkenv, --testjob, --workload --benchmark]"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-c', '--config',
                      metavar='CONFIG',
                      dest='config',
                      help='The user-specific configuration file. (REQUIRED)')

    parser.add_option('--checkenv',
                      dest='checkenv',
                      action="store_true",
                      help='Launches a test job to check the remote execution environment.')

    parser.add_option('--testjob',
                      dest='testjob',
                      action="store_true",
                      help='Launches a test job with a single task on the remote site.')

    parser.add_option('--benchmark',
                      dest='benchmark',
                      action="store_true",
                      help='Launches a series of test jobs to test performance and scalability.')

    parser.add_option('-w', '--workload',
                      metavar='WORKLOAD',
                      dest='workload',
                      help='Launches the tasks defined in the provided workload description file.')

    # PARSE THE CMD LINE OPTIONS
    (options, args) = parser.parse_args()

    if options.config is None:
        parser.error("You must define a configuration (-c/--config). Try --help for help.")
    
    config = imp.load_source('config', options.config)

    if options.checkenv is True:
        # RUN THE CHECK ENVIRONMENT JOB
        result = run_checkenv(config=config)
        sys.exit(result)

    elif options.testjob is True:
        # RUN THE SIM TEST JOB
        result = run_testjob(config=config) 
        sys.exit(result)

    elif options.benchmark is True:
        # RUN THE SIM BENCHMARK JOBS
        result = run_benchmark(config=config) 
        sys.exit(result)

    elif options.workload is not None:
        # RUN A WORKLOAD
        workload = imp.load_source('workload', options.workload)
        from workload import WORKLOAD 
        result = run_workload(config=config, workload=WORKLOAD)
        sys.exit(result)

    else:
        # ERROR - INVALID PARAMETERS
        parser.error("You must run either --checkenv, --testjob, --workload or --benchmark. Try --help for help.")
        sys.exit(1)

