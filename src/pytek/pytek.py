
"""
.. deprecated:: 1.1.0.0-r2

    The `~pytek.TDS3k` class has been moved up to the top level `pytek`
    module, you should use that instead.

"""
from . import TDS3k as top_TDS3k
from . import TDS3xxx as top_TDS3xxx

TDS3k = top_TDS3k
TDS3xxx = top_TDS3xxx


