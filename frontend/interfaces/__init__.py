# interfaces/__init__.py
from .api_client import APIClientInterface
from .ui_component import UIComponentInterface
from .result_formatter import ResultFormatterInterface

__all__ = ['APIClientInterface', 'UIComponentInterface', 'ResultFormatterInterface']
