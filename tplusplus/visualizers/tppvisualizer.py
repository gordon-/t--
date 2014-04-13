#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.

"""
Abstract TPP visualization class. All visualizers must inherit from it.
"""

# first we need to set the sys.path to the project's root folder
import sys
sys.path.append('../..')

import re
from datetime import datetime
from tplusplus.core import abstract_method


class TppVisualizer:
    """Implements a generic visualizer from which all other visualizers need to
    be derived.
    """

    def __init__(self):
        pass  # nothing

    def split_lines(self, text, width):
        """Splits a line into several lines, where each of the result lines is
        at most _width_ characters long, caring about word boundaries, and
        returns a list of strings.
        """
        lines = []
        if text:
            while True:
                i = width
                if len(text) <= i:  # text length is OK → add it to array and
                                    # stop splitting
                    lines.append(text)
                    text = ''
                else:
                    # search for word boundary (space actually)
                    while i > 0 and text[i] is not '':
                        i -= 1
                    # if we can’t find any space character, simply cut off at
                    # the maximum width
                    if i == 0:
                        i = width
                    # extract line
                    x = text[0:i-1]
                    # remove extracted line
                    text = text[i+1:-1]
                    # added line to array
                    lines.append(x)
                if len(text) <= 0:
                    break
        return lines

    @abstract_method
    def do_footer(self, footer_text):
        pass

    @abstract_method
    def do_header(self, header_text):
        pass

    @abstract_method
    def do_refresh(self):
        pass

    @abstract_method
    def new_page(self):
        pass

    @abstract_method
    def do_heading(self, text):
        pass

    @abstract_method
    def do_withborder(self):
        pass

    @abstract_method
    def do_horline(self):
        pass

    @abstract_method
    def do_color(self, text):
        pass

    @abstract_method
    def do_center(self, text):
        pass

    @abstract_method
    def do_right(self, text):
        pass

    @abstract_method
    def do_exec(self, cmdline):
        pass

    @abstract_method
    def do_wait(self):
        pass

    @abstract_method
    def do_beginoutput(self):
        pass

    @abstract_method
    def do_beginshelloutput(self):
        pass

    @abstract_method
    def do_endoutput(self):
        pass

    @abstract_method
    def do_endshelloutput(self):
        pass

    @abstract_method
    def do_sleep(self, time2sleep):
        pass

    @abstract_method
    def do_boldon(self):
        pass

    @abstract_method
    def do_boldoff(self):
        pass

    @abstract_method
    def do_revon(self):
        pass

    @abstract_method
    def do_revoff(self):
        pass

    @abstract_method
    def do_ulon(self):
        pass

    @abstract_method
    def do_uloff(self):
        pass

    @abstract_method
    def do_beginslieleft(self):
        pass

    @abstract_method
    def do_endslide(self):
        pass

    @abstract_method
    def do_command_prompt(self):
        pass

    @abstract_method
    def do_beginslideright(self, footer_text):
        pass

    @abstract_method
    def do_beginslidetop(self, footer_text):
        pass

    @abstract_method
    def do_beginslidebottom(self, footer_text):
        pass

    @abstract_method
    def do_sethugefont(self):
        pass

    @abstract_method
    def do_huge(self, text):
        pass

    @abstract_method
    def do_print_line(self, line):
        pass

    @abstract_method
    def do_title(self, title):
        pass

    @abstract_method
    def do_author(self, author):
        pass

    @abstract_method
    def do_date(self, date):
        pass

    @abstract_method
    def do_bgcolor(self, color):
        pass

    @abstract_method
    def do_fgcolor(self, color):
        pass

    def visualize(self, line, eop):
        """Receives a _line_, parses it if necessary, and dispatches it
        to the correct method which then does the correct processing.
        It returns whether the controller shall wait for input.
        """
        if re.match('^--heading ', line):
            text = line[9:]
            self.do_heading(text)
        elif re.match('^--withborder', line):
            self.do_withborder()
        elif re.match('^--horline', line):
            self.do_horline()
        elif re.match('^--color ', line):
            text = line[8:].strip()
            self.do_color(text)
        elif re.match('^--center ', line):
            text = line[9:].strip()
            self.do_center(text)
        elif re.match('^--right ', line):
            text = line[9:].strip()
            self.do_color(text)
        elif re.match('^--exec ', line):
            cmdline = line[6:].strip()
            self.do_exec(cmdline)
        elif re.match('^---', line):
            self.do_wait()
            return True
        elif re.match('^--beginoutput', line):
            self.do_beginoutput()
        elif re.match('^--beginshelloutput', line):
            self.do_beginshelloutput()
        elif re.match('^--endoutput', line):
            self.do_endoutput()
        elif re.match('^--endshelloutput', line):
            self.do_endshelloutput()
        elif re.match('^--sleep ', line):
            time2sleep = line[8:].strip()
            self.do_sleep(time2sleep)
        elif re.match('^--boldon', line):
            self.do_boldon()
        elif re.match('^--boldoff', line):
            self.do_boldoff()
        elif re.match('^--revon', line):
            self.do_revon()
        elif re.match('^--revoff', line):
            self.do_revoff()
        elif re.match('^--ulon', line):
            self.do_ulon()
        elif re.match('^--uloff', line):
            self.do_uloff()
        elif re.match('^--beginslideleft', line):
            self.do_beginslideleft()
        elif re.match('^--endslide', line):
            self.do_endslide()
        elif re.match('^--beginslideright', line):
            self.do_beginslideright()
        elif re.match('^--beginslidetop', line):
            self.do_beginslidetop()
        elif re.match('^--beginslidebottom', line):
            self.do_beginslidebottom()
        elif re.match('^--sethugefont ', line):
            params = line[13:].strip()
            self.do_sethugefont(params)
        elif re.match('^--huge', line):
            figlet_text = line[6:].strip()
            self.do_huge(figlet_text)
        elif re.match('^--footer ', line):
            self.footer_txt = line[8:].strip()
            self.do_footer(self.footer_text)
        elif re.match('^--header ', line):
            self.header_txt = line[8:].strip()
            self.do_header(self.header_text)
        elif re.match('^--title ', line):
            title = line[8:].strip()
            self.do_title(title)
        elif re.match('^--author ', line):
            title = line[9:].strip()
            self.do_author(title)
        elif re.match('^--date ', line):
            date = line[7:].strip()
            if date == 'today':
                date = datetime.datetime.now().strftime('%d %b %Y')
            self.do_date(date)
        elif re.match('^--bgcolor ', line):
            color = line[10:].strip()
            self.do_bgcolor(color)
        elif re.match('^--fgcolor ', line):
            color = line[10:].strip()
            self.do_fgcolor(color)
        elif re.match('^--color ', line):
            color = line[8:].strip()
            self.do_color(color)
        else:
            self.print_line(line)

        return False

    def close(self):
        pass
