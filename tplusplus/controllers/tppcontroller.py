#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gordon <gordon@starswirl>
#
# Distributed under terms of the MIT license.

"""
Abstract TPP controller class. All controllers must inherit from it.
"""

# first we need to set the sys.path to the project's root folder
import sys
sys.path.append('../..')

from tplusplus.core import abstract_method


class TppController:
    """Implements a generic controller from which all other controllers need
    to be derived.
    """

    @abstract_method
    def __init__(self):
        pass

    @abstract_method
    def close(self):
        pass

    @abstract_method
    def run(self):
        pass
