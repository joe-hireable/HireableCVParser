"""
Pytest configuration file for filtering warnings.
"""
import warnings
import pytest

def pytest_configure(config):
    """Configure pytest to ignore specific deprecation warnings."""
    # Filter out SwigPy related deprecation warnings
    warnings.filterwarnings(
        "ignore",
        message="builtin type SwigPyPacked has no __module__ attribute",
        category=DeprecationWarning,
    )
    warnings.filterwarnings(
        "ignore",
        message="builtin type SwigPyObject has no __module__ attribute",
        category=DeprecationWarning,
    )
    warnings.filterwarnings(
        "ignore", 
        message="builtin type swigvarlink has no __module__ attribute", 
        category=DeprecationWarning
    )
    
    # Filter out OpenTelemetry BoundedDict deprecation warnings
    warnings.filterwarnings(
        "ignore",
        message="Call to deprecated class BoundedDict",
        category=DeprecationWarning,
    ) 