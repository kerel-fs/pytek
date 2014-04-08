
RELEASE = 1

MAJOR = 1
MINOR = 0
PATCH = 0
SEMANTIC = 0

COPYRIGHT = 2014
YEAR = 2014
MONTH = 4
DAY = 7

#Tag options are None, "dev", and "blood-"*
# None means this is a released/tagged version.
# "dev" means this is a development version from the trunk/mainline.
# "blood" means it's on a branch. After the dash, fill in a short description
# to identify the branch.
#
# Dev and blood versions are still numbered for the *previous* version,
# because we may not know what the next version will be until we're finished.
TAG = "dev"
#TAG = None


__months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
assert((MONTH > 0) and (MONTH <= len(__months)))

def setuptools_string():
    vstr = "%d.%d.%d.%d" % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += "-x-%s" % TAG
    else:
        vstr += "-r%d" % RELEASE
    return vstr

def string():
    vstr = "%d.%d.%d.%d" % (MAJOR, MINOR, PATCH, SEMANTIC)
    if TAG is not None:
        vstr += "-%s" % TAG
    else:
        vstr += "-r%d" % RELEASE
    return vstr

def datestr():
    return "%d %s %02d" % (YEAR, __months[MONTH-1], DAY)

