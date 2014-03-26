#!/usr/bin/env python

"""This tool runs free energy calculations with Amber MMPBSA.py. 
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

from radical.ensemblemd.bac.kernel import KERNEL

DBURL = os.getenv("RADICALPILOT_DBURL")
if DBURL is None:
    print "ERROR: RADICALPILOT_DBURL (MongoDB server URL) is not defined."
    sys.exit(1)

RCONF  = ["https://raw.github.com/radical-cybertools/radical.pilot/master/configs/xsede.json",
          "https://raw.github.com/radical-cybertools/radical.pilot/master/configs/futuregrid.json"]


# ----------------------------------------------------------------------------
#
def resource_cb(origin, old_state, new_state):
    """Resource callback function: writes resource allocation state 
    changes to STDERR.
    """ 
    msg = " * Resource '%s' state changed from '%s' to '%s'.\n" % \
        (str(origin), old_state, new_state)
    sys.stderr.write(msg)

    if new_state == bigjobasync.FAILED:
        # Print the log and exit if big job has failed
        for entry in origin.log:
            print "   * LOG: %s" % entry
        sys.stderr.write("   * EXITING.\n")
        sys.exit(-1)

# ----------------------------------------------------------------------------
#
def task_cb(origin, old_state, new_state):
    """Task callback function: writes task state changes to STDERR
    """
    msg = " * Task %s state changed from '%s' to '%s'.\n" % \
        (str(origin), old_state, new_state)
    sys.stderr.write(msg)

    if new_state == bigjobasync.FAILED:
        # Print the log entry if task has failed to run
        for entry in origin.log:
            print "     LOG: %s" % entry

# ----------------------------------------------------------------------------
#
def run_workload(config, workload):
    """Runs the FE tasks defined in `workload`.
    """
    resource_name = config['resource']
    username      = config['username']
    workdir       = config['workdir']
    allocation    = config['allocation']
    numtasks      = len(workload)

    longest_runtime = 0
    for task in workload:
        if int(task['runtime']) > longest_runtime:
            longest_runtime = int(task['runtime'])

    ############################################################
    # The resource allocation
    cluster = bigjobasync.Resource(
        name       = resource_name, 
        resource   = bigjobasync.RESOURCES[resource_name],
        username   = username,
        runtime    = longest_runtime, 
        cores      = numtasks,
        workdir    = workdir,
        project_id = allocation
    )
    cluster.register_callbacks(resource_cb)
    cluster.allocate(terminate_on_empty_queue=True)

    ############################################################
    # The workload
    tasknum   = 0
    all_tasks = []

    for task in workload:

        tasknum += 1

        input_nmode = task["nmode"]
        input_com   = task["com"]
        input_rec   = task["rec"]
        input_lig   = task["lig"]
        input_traj  = task["traj"]

        kernelcfg = KERNEL["MMPBSA"]["resources"][resource_name]
        mmpbsa_task     = bigjobasync.Task(
            name        = "MMPBSA-fe-task-%s" % tasknum,
            cores       = 1,
            environment = kernelcfg["environment"],
            executable  = "/bin/bash",
            arguments   = ["-l", "-c", "\"%s && %s -i %s -cp %s -rp %s -lp %s -y %s \"" % \
                   (kernelcfg["pre_execution"], 
                    kernelcfg["executable"], 
                    os.path.basename(input_nmode),  
                    os.path.basename(input_com),  
                    os.path.basename(input_rec),  
                    os.path.basename(input_lig),  
                    os.path.basename(input_traj) 
                    )],

            input = [
                { 
                    "mode"        : bigjobasync.LINK, 
                    "origin"      : bigjobasync.REMOTE, 
                    "origin_path" : input_nmode,
                },
                {
                    "mode"        : bigjobasync.LINK, 
                    "origin"      : bigjobasync.REMOTE, 
                    "origin_path" : input_com,
                },
                {
                    "mode"        : bigjobasync.LINK, 
                    "origin"      : bigjobasync.REMOTE, 
                    "origin_path" : input_rec,
                },
                {
                    "mode"        : bigjobasync.LINK, 
                    "origin"      : bigjobasync.REMOTE, 
                    "origin_path" : input_lig,
                },
                {
                    "mode"        : bigjobasync.LINK, 
                    "origin"      : bigjobasync.REMOTE, 
                    "origin_path" : input_traj,
                },
            ],
            output = [
                {
                    "mode"             : bigjobasync.COPY, 
                    "origin_path"      : "FINAL_RESULTS_MMPBSA.dat",     
                    "destination"      : bigjobasync.LOCAL,
                    "destination_path" : "./traj-%s-FINAL_RESULTS_MMPBSA.dat" % tasknum
                }
            ]
        )
        mmpbsa_task.register_callbacks(task_cb)
        all_tasks.append(mmpbsa_task) 

    cluster.schedule_tasks(all_tasks)
    cluster.wait()

    print "DONE -- All trajectories have been processed."

    return 0

# ----------------------------------------------------------------------------
#
def run_test_job(config):
    """Runs a single FE test job.
    """

    resource_name = config['resource']
    username      = config['username']
    workdir       = config['workdir']
    allocation    = config['allocation']

    # Download the sample data from MDStack server
    sampledata = {
        "nmode.5h.py" : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/nmode.5h.py",
        "com.top.2"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/com.top.2",
        "rec.top.2"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/rec.top.2",
        "lig.top"     : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/lig.top",
        "rep1.traj"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/trajectories/rep1.traj"
    }

    try: 
        for key, val in sampledata.iteritems():
            print " * Downloading sample input data %s" % val
            urllib.urlretrieve(val, key)
    except Exception, ex:
        print "ERROR - Couldn't download sample data: %s" % str(ex)
        return 1

    ############################################################
    # The resource allocation
    cluster = bigjobasync.Resource(
        name       = resource_name, 
        resource   = bigjobasync.RESOURCES[resource_name],
        username   = username,
        runtime    = 60, 
        cores      = 16, 
        workdir    = workdir,
        project_id = allocation
    )
    cluster.register_callbacks(resource_cb)
    cluster.allocate(terminate_on_empty_queue=True)

    ############################################################
    # The test task
    output_file = "./MMPBSA-test-task-%s" % str(uuid.uuid4())

    kernelcfg = KERNEL["MMPBSA"]["resources"][resource_name]

    mmpbsa_test_task = bigjobasync.Task(
        name        = "MMPBSA-fe-test-task",
        cores       = 1,
        environment = kernelcfg["environment"],
        executable  = "/bin/bash",
        arguments   = ["-l", "-c", "\"%s && %s -i nmode.5h.py -cp com.top.2 -rp rec.top.2 -lp lig.top -y rep1.traj \"" % \
            (kernelcfg["pre_execution"], kernelcfg["executable"])],

        input = [
            { 
                "mode"        : bigjobasync.COPY,
                "origin"      : bigjobasync.LOCAL,
                "origin_path" : "/%s/nmode.5h.py" % os.getcwd(),
            },
            {
                "mode"        : bigjobasync.COPY, 
                "origin"      : bigjobasync.LOCAL, 
                "origin_path" : "/%s/com.top.2" % os.getcwd(),
            },
            {
                "mode"        : bigjobasync.COPY, 
                "origin"      : bigjobasync.LOCAL, 
                "origin_path" : "/%s/rec.top.2" % os.getcwd(),
            },
            {
                "mode"        : bigjobasync.COPY, 
                "origin"      : bigjobasync.LOCAL, 
                "origin_path" : "/%s/lig.top" % os.getcwd(),
            },
            {
                "mode"        : bigjobasync.COPY, 
                "origin"      : bigjobasync.LOCAL, 
                "origin_path" : "/%s/rep1.traj" % os.getcwd(),
            },
        ], 

        output = [
            {
                "mode"              : bigjobasync.COPY, 
                "origin_path"       : "STDOUT" ,      
                "destination"       : bigjobasync.LOCAL,
                "destination_path"  : output_file,
                "trasfer_if_failed" : True
            }
        ]
    )
    mmpbsa_test_task.register_callbacks(task_cb)

    cluster.schedule_tasks([mmpbsa_test_task])
    cluster.wait()

    try: 
        with open(output_file, 'r') as content_file:
            content = content_file.read()
            print content
        os.remove(output_file)

        for key, val in sampledata.iteritems():
            os.remove("./%s" % key)

    except Exception:
        pass

    return 0

# ----------------------------------------------------------------------------
#
def run_sanity_check(config):
    """Runs a simple job that performs some sanity tests, determines 
    AMBER version, etc.
    """
    resource_name  = config['resource']
    cores_per_node = config['cores_per_node']
    username       = config['username']
    allocation     = config['allocation']

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
        pdesc.resource   = resource_name
        pdesc.runtime    = 15 # minutes
        pdesc.cores      = int(cores_per_node) * 1 # one node 
        pdesc.allocation = allocation

        pilot = pmgr.submit_pilots(pdesc)

        ############################################################
        # The test task
        kernelcfg = KERNEL["MMPBSA"]["resources"][resource_name]

        cudesc = radical.pilot.ComputeUnitDescription()
        cudesc.environment = kernelcfg["environment"]
        cudesc.executable = "/bin/bash"
        cudesc.arguments = ["-l", "-c", "\"%s && echo -n MMPBSA path: && which %s && echo -n MMPBSA version: && %s --version\"" % \
                (kernelcfg["pre_execution"], kernelcfg["executable"], kernelcfg["executable"]) ]
        cudesc.cores = 1


        umgr = radical.pilot.UnitManager(session=session,
            scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
        umgr.register_callback(task_cb)
        umgr.add_pilots(pilot)

        umgr.submit_units(cudesc)
        umgr.wait_units()

        session.close()

    except Exception, ex:
        print "ERROR during execution: %s" % str(ex)
        session.close()
        return 1

    ############################################################
    # Output the result
    try: 
        with open(output_file, 'r') as content_file:
            content = content_file.read()
            print content
        os.remove(output_file)

    except Exception:
        pass

    return 0

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
                      help='Launches a test job with a single FE calculation.')

    parser.add_option('-c', '--config',
                      metavar='CONFIG',
                      dest='config',
                      help='The machine / resource configuration file. (REQUIRED)')


    parser.add_option('-w', '--workload',
                      metavar='WORKLOAD',
                      dest='workload',
                      help='Launches the FE tasks defined in the provided WORKLOAD file.')

    # PARSE THE CMD LINE OPTIONS
    (options, args) = parser.parse_args()

    if options.config is None:
        parser.error("You must define a configuration (-c/--config). Try --help for help.")
    
    config = imp.load_source('config', options.config)

    if options.checkenv is True:
        # RUN THE CHECK ENVIRONMENT JOB
        result = run_sanity_check(config=config.CONFIG)
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

