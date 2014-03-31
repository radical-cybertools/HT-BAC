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

from radical.ensemblemd.bac.fecalc import run_benchmark
from radical.ensemblemd.bac.fecalc import run_checkenv
from radical.ensemblemd.bac.fecalc import run_testjob

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
                      help='Launches a test job with a single calculation task on the remote site.')

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
        # RUN THE FE TEST JOB
        result = run_testjob(config=config) 
        sys.exit(result)

    elif options.benchmark is True:
        # RUN THE FE BENCHMARK JOBS
        result = run_benchmark(config=config) 
        sys.exit(result)

    elif options.workload is not None:
        # RUN A WORKLOAD
        workload = __import__(options.workload.split(".")[0])
        from workload import WORKLOAD 
        result = run_workload(config=config, workload=WORKLOAD)
        sys.exit(result)

    else:
        # ERROR - INVALID PARAMETERS
        parser.error("You must run either --checkenv, --testjob, --workload or --benchmark. Try --help for help.")
        sys.exit(1)

