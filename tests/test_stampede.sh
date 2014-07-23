#! /bin/bash

export RADICAL_PILOT_VERBOSE=info

htbac-fecalc --config=config-stampede.py --checkenv \
&& \
htbac-fecalc --config=config-stampede.py --testjob \
&& \
rm -rf lig.top nmode.5h.py rec.top.2 com.top.2 trajectories
