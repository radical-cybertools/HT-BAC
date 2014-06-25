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
from radical.ensemblemd.htbac.common import BatchRunner

# ----------------------------------------------------------------------------
#
def run_benchmark(config):
    # """Runs a workload.
    # """
    server      = config.SERVER
    resource    = config.RESOURCE
    username    = config.USERNAME
    allocation  = config.ALLOCATION

    dbname           = config.FECALC_BENCHMARK_DBNAME
    pilot_sizes      = config.FECALC_BENCHMARK_PILOT_SIZES
    task_parallelism = config.FECALC_BENCHMARK_TASK_PARALLELISM

    for ps in pilot_sizes:
        for tp in task_parallelism:
            tasks = ps / tp

            # Set up the session:
            session = radical.pilot.Session(database_url=server, database_name=dbname)

            # Add an ssh identity to the session.
            cred = radical.pilot.SSHCredential()
            cred.user_id = username
            session.add_credential(cred)

            print "Pilot size: %3s Task parallelism: %3s Num tasks: %3s. Session ID: %s" % (ps, tp, tasks, session.uid)

            workload = []

            for n in range(0, tasks):
                input_nmode = config.FECALC_BENCHMARK_INPUT_DATA[0]
                nmode_basen = os.path.basename(input_nmode)

                input_com   = config.FECALC_BENCHMARK_INPUT_DATA[1]
                com_basen   = os.path.basename(input_com)

                input_rec   = config.FECALC_BENCHMARK_INPUT_DATA[2]
                rec_basen   = os.path.basename(input_rec)

                input_lig   = config.FECALC_BENCHMARK_INPUT_DATA[3]
                lig_basen   = os.path.basename(input_lig)

                input_traj  = config.FECALC_BENCHMARK_INPUT_DATA[4]
                traj_basen  = os.path.basename(input_traj)

                mdtd = MDTaskDescription()
                mdtd.kernel = "MMPBSA"
                mdtd.arguments = "-i {0} -cp {1} -rp {2} -lp {3} -y {4}".format(nmode_basen, com_basen, rec_basen, lig_basen, traj_basen)

                if config.FECALC_BENCHMARK_INPUT_DATA_LOCATION.lower() == "remote":
                    mdtd.copy_local_input_data = [input_nmode, input_com, input_rec, input_lig, input_traj]

                mdtd_bound = mdtd.bind(resource=resource)

                mmpbsa_task = radical.pilot.ComputeUnitDescription()
                mmpbsa_task.environment = mdtd_bound.environment 
                mmpbsa_task.pre_exec    = mdtd_bound.pre_exec
                mmpbsa_task.executable  = mdtd_bound.executable
                mmpbsa_task.arguments   = mdtd_bound.arguments
                mmpbsa_task.mpi         = mdtd_bound.mpi
                mmpbsa_task.cores       = tp
                mmpbsa_task.name        = "task-{0}".format(n)

                if config.FECALC_BENCHMARK_INPUT_DATA_LOCATION.lower() == "local":
                    # No remote files. All files are local and need to be transferred
                    mmpbsa_task.input_data  = [input_nmode, input_com, input_rec, input_lig, input_traj]

                workload.append(mmpbsa_task)

            # EXECUTE THE BENCHMARK WORKLOAD
            pmgr = radical.pilot.PilotManager(session=session)
            #pmgr.register_callback(resource_cb)

            ############################################################
            # The pilot description
            pdesc = radical.pilot.ComputePilotDescription()
            pdesc.resource   = resource
            pdesc.runtime    = 30
            pdesc.cores      = ps
            pdesc.project    = allocation
            pdesc.cleanup    = True
            pdesc.sandbox    = "/work/00988/tg802352/radical.pilot.sandbox"
            pdesc.cleanup    = True

            pilot = pmgr.submit_pilots(pdesc)

            umgr = radical.pilot.UnitManager(session=session, scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
            #umgr.register_callback(task_cb)
            umgr.add_pilots(pilot)

            tasks = umgr.submit_units(workload)
            print " o STARTED "
            umgr.wait_units()
            print " o FINISHED"

            pilot.cancel()

            # Close the session.
            session.close(delete=False)

    sys.exit(0)

