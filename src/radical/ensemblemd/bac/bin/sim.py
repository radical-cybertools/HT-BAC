#!/usr/bin/env python

"""This tool ... namd.
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

DBURL = os.getenv("RADICALPILOT_DBURL")
if DBURL is None:
    print "ERROR: RADICALPILOT_DBURL (MongoDB server URL) is not defined."
    sys.exit(1)

RCONF  = ["https://raw.github.com/radical-cybertools/radical.pilot/master/configs/xsede.json",
          "https://raw.github.com/radical-cybertools/radical.pilot/master/configs/futuregrid.json"]


# ----------------------------------------------------------------------------
#
def run_sanity_check(config):
    """Runs a simple job that performs some sanity tests, determines 
    AMBER version, etc.
    """
    maxcpus = config.MAXCPUS
    resource = config.RESOURCE
    username = config.USERNAME
    allocation = config.ALLOCATION

    resource_params = KERNEL[resource]["params"]
    cores_per_node = resource_params["cores_per_node"]

    kernelcfg = KERNEL[resource]["kernel"]["namd"]

    session = radical.pilot.Session(database_url=DBURL)

    try:
        # Add an ssh identity to the session.
        cred = radical.pilot.SSHCredential()
        cred.user_id = username
        session.add_credential(cred)

        ############################################################
        # The resource allocation
        pmgr = radical.pilot.PilotManager(session=session, resource_configurations=RCONF)
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

        task_desc = radical.pilot.ComputeUnitDescription()
        task_desc.environment = kernelcfg["environment"]
        task_desc.executable = "/bin/bash"
        task_desc.arguments = ["-l", "-c", "\"%s && echo -n NAMD path: && which %s \"" % \
                (kernelcfg["pre_execution"], kernelcfg["executable"]) ]
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

# ----------------------------------------------------------------------------
#
def main():

    usage = "usage: %prog --config [--checkenv, --testjob, --workload]"
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
                      help='Launches a test job with a single calculation task on the remote site.')

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
        result = run_sanity_check(config=config)
        sys.exit(result)

    elif options.testjob is True:
        # RUN THE FE TEST JOB
        result = run_test_job(config=config.CONFIG) 
        sys.exit(result)

    elif options.workload is not None:
        # RUN A WORKLOAD
        workload = __import__(options.workload.split(".")[0])
        from workload import WORKLOAD 
        result = run_workload(config=config.CONFIG, workload=WORKLOAD)
        sys.exit(result)

    else:
        # ERROR - INVALID PARAMETERS
        parser.error("You must run either --checkenv, --testjob or --workload. Try --help for help.")
        sys.exit(1)