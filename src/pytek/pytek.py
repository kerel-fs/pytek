
"""
.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.




.. py:class:: TDS3k

This is simply a synonym for `pytek.TDS3k` to support the incorrect placement
of this class in verion 1.0.0.0-r1.

.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.



.. py:class:: TDS3xxx

This is simply a synonym for `pytek.TDS3xxx` to support the incorrect placement
of this class in verion 1.0.0.0-r1.

.. deprecated:: 1.1.0.0-r2

    The contents of this submodule have been moved up to the top level `pytek`
    module, you should use that instead. They will be retained here as aliases
    in perpetuity to support the old interface, but the new locations are
    preferred for the sake of simpler imports.



"""
from . import TDS3k as top_TDS3k
from . import TDS3xxx as top_TDS3xxx


TDS3k = top_TDS3k
TDS3xxx = top_TDS3xxx


