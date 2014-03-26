#!/usr/bin/env python

"""This tool ...
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

# ----------------------------------------------------------------------------
#
def main():

    usage = "usage: %prog --config [--checkenv, --testjob, --workload]"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('--checkenv',
                      dest='checkenv',
                      action="store_true",
                      help='Launches a test job to check the execution environment.')

    parser.add_option('--testjob',
                      dest='testjob',
                      action="store_true",
                      help='Launches a test job with a small test simulation.')

    parser.add_option('-c', '--config',
                      metavar='CONFIG',
                      dest='config',
                      help='The machine / resource configuration file. (REQUIRED)')


    parser.add_option('-w', '--workload',
                      metavar='WORKLOAD',
                      dest='workload',
                      help='Launches the simulation tasks defined in the provided WORKLOAD file.')

    # PARSE THE CMD LINE OPTIONS
    (options, args) = parser.parse_args()

    if options.config is None:
        parser.error("You must define a configuration (-c/--config). Try --help for help.")
    
    config = imp.load_source('config', options.config)

    if options.checkenv is True:
        # RUN THE CHECK ENVIRONMENT JOB
        result = 0 # run_sanity_check(config=config.CONFIG)
        sys.exit(result)

    elif options.testjob is True:
        # RUN THE FE TEST JOB
        result = 0 # run_test_job(config=config.CONFIG) 
        sys.exit(result)

    elif options.workload is not None:
        # RUN A WORKLOAD
        workload = __import__(options.workload.split(".")[0])
        from workload import WORKLOAD 
        result = 0 # run_workload(config=config.CONFIG, workload=WORKLOAD)
        sys.exit(result)

    else:
        # ERROR - INVALID PARAMETERS
        parser.error("You must run either --checkenv, --testjob or --workload. Try --help for help.")
        sys.exit(1)

