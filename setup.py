#!/usr/bin/env python

"""Setup file for HT-BAC Tools.
"""

__author__    = "Ole Weidner"
__email__     = "ole.weidner@rutgers.edu"
__copyright__ = "Copyright 2014, The RADICAL Project at Rutgers"
__license__   = "MIT"


""" Setup script. Used by easy_install and pip. """

import os
import sys
import subprocess

from setuptools import setup, find_packages, Command

#-----------------------------------------------------------------------------
# check python version. we need > 2.5, <3.x
if  sys.hexversion < 0x02060000 or sys.hexversion >= 0x03000000:
    raise RuntimeError("HT-BAC requires Python 2.6 or higher")

#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

#-----------------------------------------------------------------------------
setup_args = {
    'name'             : 'radical.ensemblemd.htbac',
    'version'          : (read('VERSION')),
    'description'      : "HT-BAC is a tool for molecular dynamics binding affinity calculations.",
    'long_description' : (read('README.md') + '\n\n' + read('CHANGES.md')),
    'author'           : 'RADICAL Group at Rutgers University',
    'author_email'     : 'ole.weidner@rutgers.edu',
    'maintainer'       : "Ole Weidner", 
    'maintainer_email' : 'ole.weidner@rutgers.edu',
    'url'              : 'https://github.com/radical-cybertools/HT-BAC',
    'license'          : 'MIT',
    'keywords'         : "molecular dynamics binding affinity calculations",
    'classifiers'      :  [
        'Development Status   :: 5 - Production/Stable',
        'Intended Audience    :: Developers',
        'Environment          :: Console',
        'License              :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic                :: Utilities',
        'Topic                :: System :: Distributed Computing',
        'Operating System     :: MacOS :: MacOS X',
        'Operating System     :: POSIX',
        'Operating System     :: Unix'
    ],

    'entry_points': {
        'console_scripts': 
            ['htbac-fecalc = radical.ensemblemd.htbac.bin.fecalc:main',
             'htbac-sim    = radical.ensemblemd.htbac.bin.sim:main',
             'htbac-nmode  = radical.ensemblemd.htbac.bin.nmode:main']
    },

    'namespace_packages' : ['radical', 'radical.ensemblemd'],
    'packages'           : find_packages('src'),
    'package_dir'        : {'': 'src'},  

    'data_files'         : [('radical/ensemblemd/htbac', ['VERSION'])],

    'install_requires'   : ['radical.pilot'],

    'tests_require'      : ['radical.pilot', 'nose'],
    'test_suite'         : 'radical.ensemblemd.htbac.tests',

    'zip_safe'           : False,
}

#-----------------------------------------------------------------------------

setup (**setup_args)

#-----------------------------------------------------------------------------
