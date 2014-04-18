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

    # resource   = config.RESOURCE
    # username   = config.USERNAME
    # allocation = config.ALLOCATION

    # resource_params = KERNEL[resource]["params"]
    # cores_per_node = resource_params["cores_per_node"]

    # kernelcfg = KERNEL[resource]["kernel"]["mmpbsa"]

    # # Download the sample data from MDStack server
    # sampledata = {
    #     "nmode.5h.py" : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/nmode.5h.py",
    #     "com.top.2"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/com.top.2",
    #     "rec.top.2"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/rec.top.2",
    #     "lig.top"     : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/lig.top",
    #     "rep1.traj"   : "http://repex2.tacc.utexas.edu/cybertools/sampledata/MMBPSA/trajectories/rep1.traj"
    # }

    # try: 
    #     for key, val in sampledata.iteritems():
    #         print " * Downloading sample input data %s" % val
    #         urllib.urlretrieve(val, key)
    # except Exception, ex:
    #     print "ERROR - Couldn't download sample data: %s" % str(ex)
    #     return 1

    # ############################################################
    # try:
    #     # Add an ssh identity to the session.
    #     cred = radical.pilot.SSHCredential()
    #     cred.user_id = username
    #     session.add_credential(cred)

    #     ############################################################
    #     # The resource allocation
    #     pmgr = radical.pilot.PilotManager(session=session, resource_configurations=RCONF)
    #     pmgr.register_callback(resource_cb)

    #     pdesc = radical.pilot.ComputePilotDescription()
    #     pdesc.resource   = resource
    #     pdesc.runtime    = 15 # minutes
    #     pdesc.cores      = int(cores_per_node) * 1 # one node 
    #     pdesc.project    = allocation
    #     pdesc.cleanup    = True

    #     pilot = pmgr.submit_pilots(pdesc)

    # ############################################################
    # # The test task
    # output_file = "./MMPBSA-test-task-%s" % str(uuid.uuid4())

    # kernelcfg = KERNEL["MMPBSA"]["resources"][resource_name]

    # mmpbsa_test_task = bigjobasync.Task(
    #     name        = "MMPBSA-fe-test-task",
    #     cores       = 1,
    #     environment = kernelcfg["environment"],
    #     executable  = "/bin/bash",
    #     arguments   = ["-l", "-c", "\"%s && %s -i nmode.5h.py -cp com.top.2 -rp rec.top.2 -lp lig.top -y rep1.traj \"" % \
    #         (kernelcfg["pre_execution"], kernelcfg["executable"])],

    #     input = [
    #         { 
    #             "mode"        : bigjobasync.COPY,
    #             "origin"      : bigjobasync.LOCAL,
    #             "origin_path" : "/%s/nmode.5h.py" % os.getcwd(),
    #         },
    #         {
    #             "mode"        : bigjobasync.COPY, 
    #             "origin"      : bigjobasync.LOCAL, 
    #             "origin_path" : "/%s/com.top.2" % os.getcwd(),
    #         },
    #         {
    #             "mode"        : bigjobasync.COPY, 
    #             "origin"      : bigjobasync.LOCAL, 
    #             "origin_path" : "/%s/rec.top.2" % os.getcwd(),
    #         },
    #         {
    #             "mode"        : bigjobasync.COPY, 
    #             "origin"      : bigjobasync.LOCAL, 
    #             "origin_path" : "/%s/lig.top" % os.getcwd(),
    #         },
    #         {
    #             "mode"        : bigjobasync.COPY, 
    #             "origin"      : bigjobasync.LOCAL, 
    #             "origin_path" : "/%s/rep1.traj" % os.getcwd(),
    #         },
    #     ], 

    #     output = [
    #         {
    #             "mode"              : bigjobasync.COPY, 
    #             "origin_path"       : "STDOUT" ,      
    #             "destination"       : bigjobasync.LOCAL,
    #             "destination_path"  : output_file,
    #             "trasfer_if_failed" : True
    #         }
    #     ]
    # )
    # mmpbsa_test_task.register_callbacks(task_cb)

    # cluster.schedule_tasks([mmpbsa_test_task])
    # cluster.wait()

    # try: 
    #     with open(output_file, 'r') as content_file:
    #         content = content_file.read()
    #         print content
    #     os.remove(output_file)

    #     for key, val in sampledata.iteritems():g
    #         os.remove("./%s" % key)

    # except Exception:
    #     pass

    return 0
