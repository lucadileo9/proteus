"""
Adapter layer — wraps external libraries behind the uniform BaseAdapter interface.

Adapter pattern (GoF):
    Target  → BaseAdapter
    Adapter → JSONAdapter, YAMLAdapter, EnvAdapter
    Adaptee → json (stdlib), yaml (PyYAML), dotenv (python-dotenv)
"""

from .base import BaseAdapter
from .env_adapter import EnvAdapter
from .json_adapter import JSONAdapter
from .yaml_adapter import YAMLAdapter

__all__ = [
    "BaseAdapter",
    "JSONAdapter",
    "YAMLAdapter",
    "EnvAdapter",
]
