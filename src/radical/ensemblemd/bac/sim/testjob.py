#!/usr/bin/env python

"""This module implements radical-bac-fecalc --testjob.
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

import radical.pilot
from radical.ensemblemd.bac.common import run_testjob as testjob
from radical.ensemblemd.bac.kernel import KERNEL


# ----------------------------------------------------------------------------
#
def run_testjob(config):
    # """Runs a test job.
    # """
    return testjob(
        config=config,
        pilot_description=None,
        cu_description=None)