"""
Inverse Kinematics Module for Spider Robot

This module provides inverse and forward kinematics calculations
for spider robot legs, along with visualization utilities.
"""

from .spider_leg import SpiderLeg
from .leg_plotter import plot_base, plot_leg, spider_show

__all__ = [
    'SpiderLeg',
    'plot_base',
    'plot_leg',
    'spider_show',
]
