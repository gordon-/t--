#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gordon <gordon@starswirl>
#
# Distributed under terms of the MIT license.

"""
NCurses visualizer for T++ (based on Urwid)
"""

# first we need to set the sys.path to the project's root folder
import sys
sys.path.append('../..')

import subprocess
import urwid
from tplusplus.visualizers.tppvisualizer import TppVisualizer


class NcursesVisualizer(TppVisualizer):

    def __init__(self, outputfile):
        # self.figletfont = 'Half Block 7x7'
        self.figletfont = 'standard'
        self.lines = [[]]
        self.footer = urwid.AttrMap(urwid.Text(''), '')
        self.page_number = 0
        self.cur_page = 0
        self.ul = False
        self.bold = False
        self.rev = False

    def keyboard_input(self, input):
        if input in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()
        elif input in (' ', 'down'):
            if self.cur_page < len(self.pages)-1:
                self.cur_page += 1
                self.content = urwid.Pile(self.pages[self.cur_page])
                self.frame.set_body(urwid.Filler(self.content, valign='top'))
                self.footer = urwid.AttrMap(urwid.Text('Slide [%s/%s]' %
                                            ((self.cur_page + 1),
                                             len(self.pages))), '')
                self.frame.set_footer(self.footer)
                self.loop.draw_screen()
            else:
                sys.exit(0)
        elif input is 'up':
            if self.cur_page < len(self.pages):
                self.cur_page -= 1
                self.content = urwid.Pile(self.pages[self.cur_page])
                self.frame.set_body(urwid.Filler(self.content, valign='top'))
                self.footer = urwid.AttrMap(urwid.Text('Slide [%s/%s]' %
                                                       ((self.cur_page + 1),
                                                        len(self.pages))),
                                            '')
                self.frame.set_footer(self.footer)
                self.loop.draw_screen()
            else:
                raise urwid.ExitMainLoop()

    def do_footer(self, footer_text):
        pass

    def do_header(self, footer_text):
        pass

    def do_refresh(self):
        pass

    def new_page(self):
        self.lines.append([])
        self.page_number += 1

    def do_heading(self, text):
        pass

    def do_withborder(self):
        pass

    def do_horline(self):
        self.lines[self.page_number].append(urwid.Divider('—'))
        pass

    def do_color(self, text):
        pass

    def do_exec(self, cmdline):
        op = subprocess.Popen(cmdline,
                              shell=True,
                              stdout=subprocess.PIPE).stdout
        for line in op.read().decode().split('\n'):
            self.print_line(line)
        op.close()
        pass

    def do_wait(self):
        pass

    def do_beginoutput(self):
        if not hasattr(self, 'output'):
            self.output = []

    def do_beginshelloutput(self):
        if not hasattr(self, 'shell_output'):
            self.shell_output = []

    def do_endoutput(self):
        if hasattr(self, 'output'):
            output = urwid.LineBox(urwid.Pile(self.output))
            self.lines[self.page_number].append(output)
            del self.output

    def do_endshelloutput(self):
        if hasattr(self, 'shell_output'):
            output = urwid.LineBox(urwid.Pile(self.shell_output))
            self.lines[self.page_number].append(output)
            del self.shell_output

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
        self.ul = True

    def do_uloff(self):
        self.ul = False

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
        # bigtext = urwid.BigText(text, self.figletfont)
        # bigtext = urwid.Padding(bigtext, 'left', width='clip')
        # bigtext = urwid.Filler(bigtext, 'bottom')
        # bigtext = urwid.BoxAdapter(bigtext, 7)
        # self.lines[self.page_number].append(bigtext)
        op = subprocess.Popen('figlet -C utf8 -f %s -w 200 "%s"' %
                              (self.figletfont, text),
                              shell=True,
                              stdout=subprocess.PIPE).stdout
        for line in op.read().decode().split('\n'):
            self.print_line(line)
        op.close()

    def print_line(self, line):
        if self.ul:
            line = ('underline', line)
        if self.bold:
            line = ('bold', line)
        if hasattr(self, 'output'):
            self.output.append(urwid.Text(line))
        elif hasattr(self, 'shell_output'):
            self.shell_output.append(urwid.Text(line))
        else:
            self.lines[self.page_number].append(urwid.Text(line))

    def do_center(self, text):
        if hasattr(self, 'output'):
            self.output.append(urwid.Text(text, align='center'))
        elif hasattr(self, 'shell_output'):
            self.shell_output.append(urwid.Text(text, align='center'))
        else:
            self.lines[self.page_number].append(urwid.Text(text,
                                                           align='center'))

    def do_right(self, text):
        if hasattr(self, 'output'):
            self.output.append(urwid.Text(text, align='right'))
        elif hasattr(self, 'shell_output'):
            self.shell_output.append(urwid.Text(text, align='right'))
        else:
            self.lines[self.page_number].append(urwid.Text(text,
                                                           align='right'))

    def do_title(self, title):
        self.lines[self.page_number].append(urwid.Text(('bold', title),
                                                       align='center'))

    def do_author(self, author):
        self.lines[self.page_number].append(urwid.Text(('bold', author),
                                                       align='center'))

    def do_date(self, date):
        self.lines[self.page_number].append(urwid.Text(('bold', date),
                                                       align='center'))

    def do_bgcolor(self, color):
        pass

    def do_fgcolor(self, color):
        pass

    def close(self):
        self.pages = []
        # for page in self.lines:
        #     self.pages.append(urwid.Text('\n'.join(page)))
        self.pages = self.lines
        # print(self.pages)
        palette = [('body', 'white', 'black', 'standout'),
                   ('footer', 'black', 'light gray'),
                   ]
        self.content = urwid.Pile(self.pages[0])
        self.footer = urwid.AttrMap(urwid.Text('Slide [1/%s]' %
                                    len(self.pages)), '')

        self.frame = urwid.Frame(urwid.Filler(self.content, valign='middle'),
                                 footer=self.footer)
        self.box = urwid.LineBox(self.frame)
        self.loop = urwid.MainLoop(self.box,
                                   palette,
                                   unhandled_input=self.keyboard_input)
        self.loop.run()
