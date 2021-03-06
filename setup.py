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
#
def get_version():

    short_version = None  # 0.4.0
    long_version  = None  # 0.4.0-9-g0684b06

    try:
        import subprocess as sp
        import re

        srcroot       = os.path.dirname (os.path.abspath (__file__))
        VERSION_MATCH = re.compile (r'(([\d\.]+)\D.*)')

        # attempt to get version information from git
        p   = sp.Popen ('cd %s && git describe --tags --always' % srcroot,
                        stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        out = p.communicate()[0]


        if  p.returncode != 0 or not out :

            # the git check failed -- its likely that we are called from
            # a tarball, so use ./VERSION instead
            out=open ("%s/VERSION" % ".", 'r').read().strip()


        # from the full string, extract short and long versions
        v = VERSION_MATCH.search (out)
        if v:
            long_version  = v.groups ()[0]
            short_version = v.groups ()[1]


        # sanity check if we got *something*
        if  not short_version or not long_version :
            sys.stderr.write ("Cannot determine version from git or ./VERSION\n")
            import sys
            sys.exit (-1)


        # make sure the version files exist for the runtime version inspection
        open ('%s/VERSION' % srcroot, 'w').write (long_version+"\n")
        open ('%s/src/radical/ensemblemd/htbac/VERSION' % srcroot, 'w').write (long_version+"\n")


    except Exception as e :
        print 'Could not extract/set version: %s' % e
        import sys
        sys.exit (-1)

    return short_version, long_version


short_version, long_version = get_version ()

#-----------------------------------------------------------------------------
# check python version. we need > 2.5, <3.x
if  sys.hexversion < 0x02050000 or sys.hexversion >= 0x03000000:
    raise RuntimeError("Sinon requires Python 2.x (2.5 or higher)")

#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

#-----------------------------------------------------------------------------
setup_args = {
    'name'             : 'radical.ensemblemd.htbac',
    'version'          : short_version,
    'description'      : "BAC is a tool for molecular dynamics binding affinity calculations.",
    'long_description' : (read('README.md') + '\n\n' + read('CHANGES.md')),
    'author'           : 'RADICAL Group at Rutgers University',
    'author_email'     : 'ole.weidner@rutgers.edu',
    'maintainer'       : "Ole Weidner", 
    'maintainer_email' : 'ole.weidner@rutgers.edu',
    'url'              : 'https://github.com/radical-cybertools',
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
            ['htbac-fecalc   = radical.ensemblemd.htbac.bin.fecalc:main',
             'htbac-simchain = radical.ensemblemd.htbac.bin.simchain:main']
    },

#    'dependency_links': [
#      'git+ssh://git@github.com/radical-cybertools/radical.ensemblemd.mdkernels.git@release#egg=radical.ensemblemd.mdkernels'
#     ],

    'namespace_packages': ['radical', 'radical.ensemblemd'],
    'packages'    :       ['radical', 
                           'radical.ensemblemd', 
                           'radical.ensemblemd.htbac', 
                           'radical.ensemblemd.htbac.fecalc', 
                           'radical.ensemblemd.htbac.tests', 
                           'radical.ensemblemd.htbac.simchain', 
                           'radical.ensemblemd.htbac.common',
                           'radical.ensemblemd.htbac.bin'],
    'package_dir' :       {'': 'src'},  

    'package_data'     :  {'': ['*.sh', 'VERSION', 'VERSION.git']},
    'install_requires' :  ['radical.pilot', 'setuptools>=1'],

    'zip_safe'         : False,
}

#-----------------------------------------------------------------------------

setup (**setup_args)

#-----------------------------------------------------------------------------
