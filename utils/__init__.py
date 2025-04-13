"""
Common utilities for the CV optimizersystem.

This package contains various helper utilities used across the application.
"""
import warnings

# Suppress specific deprecation warnings
warnings.filterwarnings(
    "ignore",
    message="Call to deprecated class BoundedDict",
    category=DeprecationWarning,
)
