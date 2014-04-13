#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gordon <gordon@starswirl>
#
# Distributed under terms of the MIT license.

"""
Basic text visualizer for T++ (mainly for tests purposes)
"""

# first we need to set the sys.path to the project's root folder
import sys
sys.path.append('../..')

import subprocess
from tplusplus.visualizers.tppvisualizer import TppVisualizer


class TextVisualizer(TppVisualizer):
    """Implements a visualizer which converts T++ source to a nicely formatted
    text file which can e.g. be used as handout
    """

    def __init__(self, outputfile):
        # try:
        #     self.f = open(self.filename, 'w+')
        # except IOError as (errno, strerr):
        #     print('Error: couldn\'t open file: {0}: {1}'
        #           .format(errno, strerr))
        #     sys.exit(1)
        self.f = outputfile
        self.output_env = False
        self.title = self.author = self.date = False
        self.figletfont = 'small'
        self.width = 80

    def do_footer(self, footer_text):
        pass

    def do_header(self, footer_text):
        pass

    def do_refresh(self):
        pass

    def new_page(self):
        self.f.write('--------------------------------------------\n')

    def do_heading(self, text):
        self.f.write('\n')
        for l in self.split_lines(text, self.width):
            self.f.write('%s\n' % l)
        self.f.write('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

    def do_withborder(self):
        pass

    def do_horline(self):
        self.f.write('********************************************\n')

    def do_color(self, text):
        pass

    def do_exec(self, cmdline):
        pass

    def do_wait(self):
        pass

    def do_beginoutput(self):
        self.f.write('---------------------------\n')
        self.output_env = True

    def do_beginshelloutput(self):
        self.do_beginoutput()

    def do_endoutput(self):
        self.f.write('---------------------------\n')
        self.output_env = False

    def do_endshelloutput(self):
        self.do_endoutput()

    def do_sleep(self, time2sleep):
        pass

    def do_boldon(self):
        pass

    def do_boldoff(self):
        pass

    def do_revon(self):
        pass

    def do_revoff(self):
        pass

    def do_ulon(self):
        pass

    def do_uloff(self):
        pass

    def do_beginslideleft(self):
        pass

    def do_endslide(self):
        pass

    def do_beginslideright(self):
        pass

    def do_beginslidetop(self):
        pass

    def do_beginslidebottom(self):
        pass

    def do_sethugefont(self, text):
        self.figletfont = text

    def do_huge(self, text):
        output_width = self.width
        if self.output_env:
            output_width -= 2
        # op = pyfiglet.Figlet(font=self.figletfont, width=output_width)
        op = subprocess.Popen('figlet -C utf8 -f %s -w %s "%s"' %
                              (self.figletfont,
                               output_width,
                               text),
                              shell=True,
                              stdout=subprocess.PIPE).stdout
        for line in op.read().decode().split('\n'):
            self.print_line(line)
        op.close()

    def print_line(self, line):
        lines = self.split_lines(line, self.width)
        for l in lines:
            if self.output_env:
                self.f.write('| %s\n' % l)
            else:
                self.f.write('%s\n' % l)

    def do_center(self, text):
        lines = self.split_lines(text, self.width)
        for line in lines:
            spaces = int((self.width - len(line)) / 2)
            if spaces < 0:
                spaces = 0
            for i in range(spaces):
                line = ' ' + line
            self.print_line(line)

    def do_right(self, text):
        lines = self.split_lines(text, self.width)
        for line in lines:
            spaces = self.width - len(line)
            if spaces < 0:
                spaces = 0
            for i in range(spaces):
                line = ' ' + line
            self.print_line(line)

    def do_title(self, title):
        self.f.write('Title: %s\n' % title)
        self.title = True
        if self.title and self.author and self.date:
            self.f.write('\n\n')

    def do_author(self, author):
        self.f.write('Author: %s\n' % author)
        self.author = True
        if self.title and self.author and self.date:
            self.f.write('\n\n')

    def do_date(self, date):
        self.f.write('Date: %s\n' % date)
        self.date = True
        if self.title and self.author and self.date:
            self.f.write('\n\n')

    def do_bgcolor(self, color):
        pass

    def do_fgcolor(self, color):
        pass

    def close(self):
        self.f.close()
