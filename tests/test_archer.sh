#! /bin/bash

export RADICAL_PILOT_VERBOSE=info 
htbac-fecalc --config=config-archer.py --checkenv
htbac-fecalc --config=config-archer.py --testjob
