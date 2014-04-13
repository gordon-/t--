#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Damien Nicolas <damien@gordon.re>
#
# Distributed under terms of the MIT license.

"""
This module reads specially-formatted files (in TPP format) and shows the
content as a presentation in text-based interface.
"""

import urwid
import sys
import re
import datetime
import subprocess
import argparse


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
    """Represents a page (aka 'slide') it T++. A page consists of a title and
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
            spaces = (self.width - len(line)) / 2
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Text Presentation Program '
                                     'Improved')
    parser.add_argument('--version', action='version', version='%(prog)s 0.8')
    parser.add_argument('-t', '--type',
                        action='store',
                        dest='type',
                        default='ncurses',
                        choices=('text', 'ncurses'),
                        help='set filetype TYPE as output format')
    parser.add_argument('-o', '--output',
                        metavar='out-file',
                        type=argparse.FileType('wt'),
                        action='store',
                        dest='output',
                        help='write output to file OUTPUT')
    parser.add_argument('file',
                        metavar='in-file',
                        type=argparse.FileType('rt'),
                        action='store',
                        help='TPP file to show')

    results = parser.parse_args()

    if results.type == 'text' and not results.output:
        parser.error('argument -o/--output is required')

    # print(results)

    visualizers = {'text': TextVisualizer, 'ncurses': NcursesVisualizer}

    try:
        ctrl = ConversionController(results.file,
                                    results.output,
                                    visualizers[results.type])
        ctrl.run()
        ctrl.close()

    except Exception as e:
        print(e.message)
