import ez_setup
ez_setup.use_setuptools()


from setuptools import setup, find_packages
import sys


sys.path.insert(0, "src")
import pytek.version


setup(
    name='pytek',
    version=pytek.version.setuptools_string(),
    description='Python API for Tektronix Oscillscopes Serial interface.',
    author='Brian Mearns',
    author_email='bmearns@ieee.org',
    url='https://bitbucket.org/bmearns/pytek/',
    license='LICENSE.txt',

    package_dir={'': 'src'},
    packages=find_packages('src'),  #Looks for __init__.py
    include_package_data = True,    #Uses MANIFEST.in
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require = {
        'serial': ["pyserial"],
        'docs': ["sphinx_rtd_theme"],
    }
)

