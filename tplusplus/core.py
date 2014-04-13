#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.

"""
Main classes for T++
"""

import urwid
import re
import subprocess


class TplusplusException(Exception):
    pass


class AbstractMethodException(Exception):
    pass


def abstract_method(fn):
    """This decorator throws an exception if the decorated function is called.
    It is intended to prevent incomplete implemetations.
    """
    def abstracted(*args, **kwargs):
        raise AbstractMethodException('Error: TppVisualizer.do_header() has '
                                      'been called directly.' % fn.__name__)
    return abstracted


class FileParser:
    """Opens a T++ source file, and splits it into the different pages"""

    def __init__(self, filename):
        self.filename = filename
        self.pages = []

    def get_pages(self):
        """Parses the specified file and returns an array of Page objects
        """
        # try:
        #     f = open(self.filename, 'r')
        # except:
        #     print('Error: couldn\'t open file: %s' % self.filename)
        #     sys.exit(1)
        f = self.filename
        number_pages = 0

        cur_page = Page('slide %s' % (number_pages + 1))
        for line in f.readlines():
            line = line.strip('\n')
            if re.match('^--##', line):
                pass  # ignore comments
            elif re.match('^--newpage', line):
                self.pages.append(cur_page)
                number_pages += 1
                name = re.search('^--newpage(.*)', line).group(1).strip()
                if name == '':
                    name = 'slide %s' % (number_pages + 1)
                cur_page = Page(name)
            else:
                cur_page.add_line(line)
        if not len(cur_page.lines):
            self.pages.append(cur_page)
        return self.pages


class Page:
    """Represents a page (aka 'slide') in T++. A page consists of a title and
    one or more lines.
    """

    def __init__(self, title):
        self.lines = []
        self.title = title
        self.cur_line = 0
        self.eop = False

    def add_line(self, line):
        """Appends a line to the page, but only if _line_ is not null
        """
        # if line:
        self.lines.append(line)

    def next_line(self):
        """Returns the next line. In case the last line is hit, then the
        end-of-page marker is set.
        """
        # print('%s : %s (%s)' % (self.title, self.cur_line, len(self.lines)))
        line = self.lines[self.cur_line]
        self.cur_line += 1
        if self.cur_line >= len(self.lines):
            self.eop = True
        return line

    def reset_eop(self):
        """Resets the end-of-page marker and sets the current line marker to the
        first line
        """
        self.cur_line = 0
        self.eop = False




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
