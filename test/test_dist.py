"""
Tests for distribution. Should be run from the top level project directory.
"""

import re
import os
import sys

sys.path.insert(0, "src")

import pytek
import pytek.version


changes_heading_re = re.compile(r'^Rel\s+(?P<release>\d+)\s+- v(?P<M>\d+).(?P<n>\d+).(?P<p>\d+).(?P<s>\d+) - (?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)\s*$')

def test_changes_dot_txt_top_version():
    with open("CHANGES.txt", "r") as changes:
        for line in changes:
            if len(line.strip()):
                mobj = changes_heading_re.match(line)
                assert(mobj is not None), line

                def match_number(group_name, against):
                    assert(int(mobj.group(group_name)) == against)

                match_number('release', pytek.version.RELEASE)
                match_number('M', pytek.version.MAJOR)
                match_number('n', pytek.version.MINOR)
                match_number('p', pytek.version.PATCH)
                match_number('s', pytek.version.SEMANTIC)
                match_number('year', pytek.version.YEAR)
                match_number('month', pytek.version.MONTH)
                match_number('day', pytek.version.DAY)

                break

            

