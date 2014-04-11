"""
The ``version`` module provides version numbering for the entire |PYTEK| package.

.. contents:: **Page Contents**
    :local:
    :depth: 3
    :backlinks: top


Versioning
-------------

The PyTek packages uses a five part version number, plus an incremental release number.
Either the version number or the release number can be used to identify
a released version of the code.


Version Number
~~~~~~~~~~~~~~~

The version number is a four part dotted number, with an optional tag on the end.
Formally, a version number looks like:

.. productionlist::
    version number: <Major>.<minor>[.<patch>[.<semantic>]][-[x-]<tag>]

With each new released version of the code, exactly one of the four numbers will
increase, and any numbers to its right will reset to 0.

The easiest way to understand version numbers is from the perspective of someone who has
written *client code*: i.e., code that makes use of a particular version of the
|PYTEK| library. From this perspective, the version number indicates whether or
not your client code can be expected to work with different versions of |PYTEK|.

.. _major-version:

Major Version
***************

The ``<Major>`` component is the **major version number**, and it describes *backward
compatibility*. Going to a *newer* version of |PYTEK|, your code should continue to work
as long as the major version doesn't change.

The major version is changed only when something is removed from the |PYTEK| public
interface. For instance, if a function is no longer supported, the major version number
would have to increase, because client code which relied on that function would no longer
work.

The major version number can be accessed through the `MAJOR` member of this module.

.. _minor-version:

Minor Version
***************

The ``<minor>`` component is the **minor version number**, and it describes *forward
compatibility*: Going to an *older* version of |PYTEK|, your code will continue to work
as long as the minor version doesn't change. (As before, your code will also work
for *newer* versions of |PYTEK|, as long as the major version number hasn't changed).

The minor version number is changed only when something is added to the |PYTEK| public
interface, for instance a new function is added. Such a change maintains *backward*
compatibility (as described above), but *loses forward compatibility*, because any client
code written again this new version may not work with an older version.

The minor version number can be accessed through the `MINOR` member of this module.

.. _patch-version:

Patch Version
***************

The ``<patch>`` component is the **patch number**, and it describes changes that
*do not affect compatibility*, either forwards or backwards. Your client code will
continue to work with an older or newer version of |PYTEK| as long as the major and minor
version numbers are the same, regardless of the patch number.

Patch changes are code changes that do not effect the interface, for instance bug-fixes
or performance enhancements. (although some bugs effect the interface and may therefore
cause a higher version number to change).

The patch number can be accessed through the `PATCH` member of this module.


.. _semantic-version:

Semantic Version
*******************

The ``<semantic>`` component is the **semantic version number**, and it describes changes
that do not affect how the code runs at all. Ths generally means that documentation or
other auxilliary files included in the package have changed.

The semantic version number can be accessed through the `SEMANTIC` member of this module.


Compatibility Summary
**********************

The following table summarizes compatibility for a hypothetical client application
built against released |PYTEK| version ``M.n.p.s``:

===========     =================== ======================
Component       Compatibile (all)   Incompatible (any)
===========     =================== ======================
Major           M                   != M
minor           >= n                < n
patch           any                 
semantic        any                 
===========     =================== ======================



Version Tag
********************

The ``<tag>`` component is the **version tag**, which is used only for non-released
code. The tag has one of the following forms:

.. productionlist::
    version tag :   << empty >>
                :   dev[-<rev>]
                :   blood-<branch>[-<rev>]

The first form is an empty tag, and is reserved for released (tagged) code only.

The second form, `"dev"`, is for non-released code in the *trunk*. This is the
main line of development. Dev code may not be completely functional, and may even
break the existing interface.

The third form, `"blood-..."`, if for non-released code on a *branch*. The `<branch>`
component of this form should be the name of the branch. This is considered
*bleeding-edge* code and may be highly unstable.

The optional ``<rev>`` component on both the second and third forms can be used to
specify a specific revision for comitted development code. This must be an globally
unambiguous identifier for the revision, for instance the change set id.

Development code
*********************

A non-empty version tag indicates a *development version* of the code. In this case, 
the four version numbers remain *unchanged* until the code is released (in which case
it is no longer development code, and the tag is changed to empty).

In other words, anytime you see a non-empty version tag, the version numbers shown
refer to version from which the development code is derived. This is done because it
is not generally known until release what the next released version number will
be, since it is not known what types of changes will be included in it.


Specifying a version number
******************************

When specifying a version number, the major and minor version numbers should always
be included. Additionally, all non-zero version numbers should be included, and
any version number to the left of a non-zero version number should be included.

The tag should always be included in the version number, with the indicated hyphen
separating the semantic version number and the tag. The only exception is for
released code, in which case the tag is empty and should be omitted, along with the
joining hyphen.

The optional ``"x-"`` shown preceding the tag in the version number is for compatibility
with setup-tools so that versions compare correctly.

The above rules will unambiguously describe any released version of the package.

Interface Version
******************************

Because any change to the public interface requires a change to either the major or minor
version numbers, the interface can be specified by a shortened two part version:

.. productionlist::
    interface version   :   <Major>.<minor>

Note that this only applies for released versions: development versions may modify the
public interface prior to changing the version numbers.
    

Release Number
~~~~~~~~~~~~~~~~~~~~~

The release number is a simple integer which increments by one for every public release
of the code. It does not convey any information about compatibility with other versions,
but it does provide a simple alternative to identifying released versions.

The release number should be written with a leading ``"r"`` or ``"rel"``. For
instance, the first release was ``"r1"``.

For release code, the release number may be used in place of the tag in the version
number. This is optional because the version number and the release number are
synonymous. However, including them both in the version string is a useful way to
provide both pieces of information.

This alternative form of the version number is:
    
.. productionlist::
    alt. version number :   <Major>.<minor>[.<patch>[.<semantic>]]-r<release>


Module Contents
--------------------

"""

RELEASE = 2
"""
The current `Release Number`_.
"""

MAJOR = 1
"""
The current :ref:`major version number <major-version>`.
"""

MINOR = 1
"""
The current :ref:`minor version number <minor-version>`.
"""

PATCH = 0
"""
The current :ref:`patch version number <patch-version>`.
"""

SEMANTIC = 0
"""
The current :ref:`semantic version number <semantic-version>`.
"""



COPYRIGHT = 2014
"""
The copyright year for the |PYTEK| code.
"""

YEAR = 2014
"""
The year in which the code was released.

.. seealso ::
    * `MONTH`
    * `DAY`
    * `datestr`

"""

MONTH = 4
"""
The month in which the code was released. This is 1 indexed, in [1, 12].

.. seealso ::
    * `YEAR`
    * `DAY`
    * `datestr`
    * `MONTH_NAMES`

"""

DAY = 10
"""
The day of the month on which the code was released.

.. seealso ::
    * `YEAR`
    * `MONTH`
    * `datestr`

"""

TAG = "dev"
#TAG = None
"""
The current `Version Tag`_.

Tag options are `None`, ``"dev"``, and ``"blood-"``

    * `None` means this is a released/tagged version.
    * ``"dev"`` means this is a development version from the trunk/mainline.
    * ``"blood-"`` means it's on a branch. After the dash, fill in the name of the branch.

Dev and blood versions are still numbered for the *previous* version,
because we may not know what the next version will be until we're finished.
"""


MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
"""
A sequence giving the names of months, for use by `datestr`. Standard values are three-letter
English-language abbreviations for the months of the Gregorian calendar.
"""


assert((MONTH > 0) and (MONTH <= len(MONTH_NAMES)))

def setuptools_string():
    """
    Returns the version string used by `setuptools`. This takes one of two forms:

    .. productionlist::
        setuptools_string   :   <Major>.<minor>.<patch>.<semantic>-x-<tag>
                            :   <Major>.<minor>.<patch>.<semantic>-r<release>

    The first form is used for development code (i.e., when `TAG` is not `None`),
    and the second it used for released code.

    This is similar to `string`, except for the additional ``x-`` for development
    versions, which is used to ensure that `setuptools` sorts versions correctly.
    (specifically, so that released versions are earler than development versions
    which are derived from them).
    """

    vstr = "%d.%d.%d.%d" % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += "-x-%s" % TAG
    else:
        vstr += "-r%d" % RELEASE
    return vstr

def tag_name():
    """
    Returns the tag name for the most recent release.
    """
    return "r%d-v%d.%d.%d.%d" % (RELEASE, MAJOR, MINOR, PATCH, SEMANTIC)

def short_string():
    """
    Returns a string describing the `Interface Version`_ (i.e., ``<Major>.<minor>``).
    """
    return "%d.%d" % (MAJOR, MINOR)

def string():
    """
    Like `setuptools_string`, except leaves out the ``x-`` for development
    versions.
    """
    vstr = "%d.%d.%d.%d" % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += "-%s" % TAG
    else:
        vstr += "-r%d" % RELEASE
    return vstr

def datestr():
    """
    Returns a simple string giving the date of release. Format
    of this string is unspecified, it intended to be human readable,
    not machine parsed. For machine processing, use the individual
    variables, as listed below.

    .. seealso ::
        * `YEAR`
        * `MONTH`
        * `DAY`
        * `MONTH_NAMES`

    """
    assert((MONTH > 0) and (MONTH <= len(MONTH_NAMES)))
    return "%d %s %02d" % (YEAR, MONTH_NAMES[MONTH-1], DAY)

