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

# ----------------------------------------------------------------------------
#
def task_cb(origin, state):
    """Task callback function: writes task state changes to STDERR
    """
    msg = " * Task %s state changed to '%s'.\n" % (origin.uid, state)
    sys.stderr.write(msg)

    #if state == radical.pilot.FAILED:
    #    print " * Task {0} (executed @ {1}) state {2}, exit code: {3}, started: {4}, finished: {5}".format(origin.uid, origin.execution_locations, origin.state, origin.exit_code, origin.start_time, origin.stop_time)
    #    print " * Task {0} STDERR: {1}".format(origin.uid, origin.stderr)