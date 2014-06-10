#!/usr/bin/env python

"""This module implements radical-bac-fecalc --benchmark. 
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import radical.pilot
from radical.ensemblemd.mdkernels import MDTaskDescription
from radical.ensemblemd.htbac.common import run_checkenv as checkenv


# -----------------------------------------------
#
def run_checkenv(config):
    """Runs a simple job that performs some sanity tests, determines
    AMBER version, etc.
    """
    resource = config.RESOURCE
    allocation = config.ALLOCATION    

    ############################################################
    # The pilot description
    #
    pdesc = radical.pilot.ComputePilotDescription()
    pdesc.resource   = resource
    pdesc.runtime    = 15 # minutes
    pdesc.cores      = 4 
    pdesc.project    = allocation
    pdesc.cleanup    = False

    ############################################################
    # The checkenv task
    #
    mdtd = MDTaskDescription()
    mdtd.kernel = "MMPBSA"
    mdtd.arguments = "--version"

    mdtd_bound = mdtd.bind(resource=resource)

    task_desc = radical.pilot.ComputeUnitDescription()
    task_desc.environment = mdtd_bound.environment 
    task_desc.pre_exec    = mdtd_bound.pre_exec
    task_desc.executable  = mdtd_bound.executable
    task_desc.arguments   = mdtd_bound.arguments
    task_desc.mpi         = mdtd_bound.mpi
    task_desc.cores       = 4

    ############################################################
    # Call the checkenv script
    #
    return checkenv(
        config=config,
        pilot_description=pdesc,
        cu_description=task_desc
    )
