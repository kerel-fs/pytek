"""
Tests for distribution. Should be run from the top level project directory.
"""

from nose.plugins.attrib import attr
import nose.tools

import re
import os
import sys

sys.path.insert(0, "src")

import pytek
import pytek.version


changes_prerelease_re = re.compile(r'^Pre[ -]?Rel\s+(?P<release>\d+)\s*$', re.I)
changes_heading_re = re.compile(r'^Rel\s+(?P<release>\d+)\s+- v(?P<M>\d+).(?P<n>\d+).(?P<p>\d+).(?P<s>\d+) - (?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)\s*$')


#TODO: Figure out an automated way to determine whether or not this is a release, to choose between the next two tests.
@nose.tools.nottest
@attr('release')
def test_empty_tag():
    assert(pytek.version.TAG is None)

@nose.tools.nottest
@attr('no-release')
def test_not_empty_tag():
    assert(pytek.version.TAG is not None)

def test_changes_dot_txt_top_version():
    with open("CHANGES.txt", "r") as changes:
        for line in changes:
            if len(line.strip()):
                mobj = changes_prerelease_re.match(line)
                def match_number(group_name, against):
                    assert(int(mobj.group(group_name)) == against), "Failed to match value of '%s': %s != %r" % (group_name, mobj.group(group_name), against)

                if mobj is not None:
                    #Pre-releases (development versions)
                    match_number('release', pytek.version.RELEASE + 1)
                    assert(pytek.version.TAG is not None)
                    
                else:
                    #If it doesn't match the pre-release, should match the release.
                    mobj = changes_heading_re.match(line)
                    assert(mobj is not None), line

                    match_number('release', pytek.version.RELEASE)
                    match_number('M', pytek.version.MAJOR)
                    match_number('n', pytek.version.MINOR)
                    match_number('p', pytek.version.PATCH)
                    match_number('s', pytek.version.SEMANTIC)
                    match_number('year', pytek.version.YEAR)
                    match_number('month', pytek.version.MONTH)
                    match_number('day', pytek.version.DAY)
                    assert(pytek.version.TAG is None)

                break

                

