def test_imports():
    """Test that main libraries can be imported."""
    import numpy as np
    import pandas as pd
    import yfinance as yf

    assert np.__version__ is not None
    assert pd.__version__ is not None
    assert yf.__version__ is not None


def test_numpy_basic():
    """Test basic numpy operations."""
    import numpy as np

    arr = np.array([1, 2, 3, 4, 5])
    assert arr.mean() == 3.0
    assert arr.sum() == 15
