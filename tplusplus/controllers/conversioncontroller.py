#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gordon <gordon@starswirl>
#
# Distributed under terms of the MIT license.

"""
The non-interactive controller for T++
"""

# first we need to set the sys.path to the project's root folder
import sys
sys.path.append('../..')

from tplusplus.core import FileParser
from tplusplus.controllers.tppcontroller import TppController


class ConversionController(TppController):
    """Implements a non-interactive controller to control non-interactive
    visualizers (i.e. those that are used for converting T++ source code into
    another format)."""

    def __init__(self, input, output, visualizer_class):
        parser = FileParser(input)
        self.pages = parser.get_pages()
        self.vis = visualizer_class(output)

    def run(self):
        for p in self.pages:
            while 1:
                line = p.next_line()
                eop = p.eop
                self.vis.visualize(line, eop)
                if eop:
                    break
            self.vis.new_page()

    def close(self):
        self.vis.close()
