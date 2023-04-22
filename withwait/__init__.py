"""
# Withwait

A simple utility to ensure that sleep operations always complete, even if an
exception happens within the with statement.

Authors:
* Miguel Guthridge

Licensed under the MIT license
"""
__all__ = [
    'wait'
]

from .__withwait import wait
