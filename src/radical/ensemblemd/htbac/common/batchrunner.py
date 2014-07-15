#!/usr/bin/env python

__author__    = "Ole Weidner <ole.weidner@rutgers.edu>"
__copyright__ = "Copyright 2013-2014, http://radical.rutgers.org"
__license__   = "MIT"

import os
import sys
import imp
import uuid
import radical.pilot

from radical.ensemblemd.htbac.callbacks import *


# -----------------------------------------------------------------------------
#
class BatchRunner(object):

    # -------------------------------------------------------------------------
    #
    def __init__(self, config):
        server = config.SERVER
        dbname = config.DBNAME

        username   = config.USERNAME
        allocation = config.ALLOCATION
        self.workdir    = config.WORKDIR

        self.session = radical.pilot.Session(database_url=server, database_name=dbname)

        # Add an ssh identity to the session.

        cred = radical.pilot.Context('ssh')
        #cred = radical.pilot.SSHCredential()
        cred.user_id = username
        self.session.add_context(cred)

    # -------------------------------------------------------------------------
    #
    def close(self):
        self.session.close()

    # -------------------------------------------------------------------------
    #
    def run(self, pilot_description, cu_descriptions):

        try:
            pmgr = radical.pilot.PilotManager(session=self.session)
            pmgr.register_callback(resource_cb)

            # Add the work dir to the cu_description
            pilot_description.sandbox = self.workdir

            pilot = pmgr.submit_pilots(pilot_description)

            umgr = radical.pilot.UnitManager(session=self.session,
                scheduler=radical.pilot.SCHED_DIRECT_SUBMISSION)
            umgr.register_callback(task_cb)
            umgr.add_pilots(pilot)

            tasks = umgr.submit_units(cu_descriptions)
            umgr.wait_units()

            return tasks

        except radical.pilot.PilotException, ex:
            print "ERROR during execution: %s" % str(ex)
            self.session.close()
            return None

