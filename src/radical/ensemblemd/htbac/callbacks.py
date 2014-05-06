#!/usr/bin/env python

"""This tool ...
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2013-2014, The RADICAL Project at Rutgers"
__license__   = "MIT"

import os, sys, uuid
import radical.pilot

# ----------------------------------------------------------------------------
#
def resource_cb(origin, state):
    """Resource callback function: writes resource allocation state 
    changes to STDERR.
    """ 
    msg = " * Resource '%s' state changed to '%s'.\n" % (origin.uid, state)
    sys.stderr.write(msg)

    if state == radical.pilot.FAILED:
        # Print the log and exit if big job has failed
        for entry in origin.log:
            print "   * LOG: %s" % entry
        sys.stderr.write("   * EXITING.\n")
        sys.exit(-1)

# ----------------------------------------------------------------------------
#
def task_cb(origin, state):
    """Task callback function: writes task state changes to STDERR
    """
    msg = " * Task %s state changed to '%s'.\n" % (origin.uid, state)
    sys.stderr.write(msg)

    if state == radical.pilot.FAILED:
        # Print the log entry if task has failed to run
        for entry in origin.log:
            print "     LOG: %s" % entry