import ez_setup
ez_setup.use_setuptools()


from setuptools import setup, find_packages
import sys

import pytek.version


setup(
    name='pytek',
    version=pytek.version.setuptools_string(),
    description='Python API for Tektronix Oscillscopes Serial interface.',
    author='Brian Mearns',
    author_email='bmearns@ieee.org',
    url='https://bitbucket.org/bmearns/pytek/',
    license='LICENSE.txt',

    packages=find_packages(),  #Looks for __init__.py
    include_package_data = True,    #Uses MANIFEST.in
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require = {
        'serial': ["pyserial"],
        'dev': ["nose==1.3.7",
                "unittest2==1.1.0",
                "coverage==4.2",
                "mock==2.0.0"],
        'docs': ["sphinx_rtd_theme"],
    }
)

