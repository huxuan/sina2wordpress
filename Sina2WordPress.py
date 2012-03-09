#!/usr/bin/python
#encoding: utf8
# +-----------------------------------------------------------------------------
# | File: Sina2WordPress.py
# | Author: huxuan
# | E-mail: i(at)huxuan.org
# | Created: 2012-12-11
# | Last modified: 2012-03-09
# | Description:
# |     Sina2WordPress is a python script to convert sina blog to wordpress.
# |     The script will crawl sina blog webpages and convert it to WXR file.
# |     Wordpress eXtended Rss (WXR) is a wordpress native supported filetype.
# |
# |     This is the main process of Sina2WordPress, which will judge whether to
# |     use Command Line Interface (CLI) or Graphical User Interface (GUI) and
# |     will call Sina2WordPressCore which will control conversion process
# |
# | Copyrgiht (c) 2012 by huxuan. All rights reserved.
# | License GPLv3
# +-----------------------------------------------------------------------------

import sys
import time

from Sina2WordPressCore import Sina2WordPressCore

class Sina2WordPressCLI():
    """Command Line Interface
    """
    def __init__(self, *args):
        """Init Sina2WordPressCLI"""
        Sina2WordPressCore(self, *args)

    def progress_init(self, msg):
        """docstring for progress_init"""
        print msg

    def progress_update(self, msg, count=0, total=0):
        """docstring for progress_update"""
        print msg

    def finish_show(self, msg):
        """docstring for finish_show"""
        print msg

def main():
    """Summary of main
    """
    if len(sys.argv) == 4:
        Sina2WordPressCLI(*sys.argv[1:])
    elif len(sys.argv) == 1:
        from Sina2WordPressGUI import Sina2WordPressGUI
        Sina2WordPressGUI()
    else:
        print '[Error] The number of parameters is invalid! 4 Needed.'

if __name__ == '__main__':
    main()
