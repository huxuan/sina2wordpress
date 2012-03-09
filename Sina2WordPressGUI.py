#!/usr/bin/python
#encoding: utf8
# +-----------------------------------------------------------------------------
# | File: Sina2WordPressGUI.py
# | Author: huxuan
# | E-mail: i(at)huxuan.org
# | Created: 2012-02-24
# | Last modified: 2012-03-09
# | Description:
# |     Graphical User Interface for Sina2WordPress
# |     This is split to allow use CLI only without wx module
# |
# | Copyrgiht (c) 2012 by huxuan. All rights reserved.
# | License GPLv3
# +-----------------------------------------------------------------------------

import wx

from Sina2WordPressCore import Sina2WordPressCore

class Sina2WordPressGUI():
    """Graphical User Interface for Sina2WordPress
    """
    def __init__(self, *args):
        """Init Sina2WordPressGUI"""
        self.app = wx.App(True)
        self.window = Sina2WordPressWindow(None, title='Sina2WordPress')
        self.app.MainLoop()

    def progress_init(self, *args, **kwargs):
        """docstring for progress_init"""
        pass

    def progress_update(self, *args, **kwargs):
        """docstring for progress_update"""
        pass

    def finish_show(self, *args, **kwargs):
        """docstring for finish_show"""
        pass

class Sina2WordPressWindow(wx.Frame, Sina2WordPressGUI):
    """Window of Sina2WordPressGUI
    """
    def __init__(self, *args, **kwargs):
        """Init Sina2WordPressWindow"""
        super(Sina2WordPressWindow, self).__init__(*args, **kwargs)

        mainSizer = wx.FlexGridSizer(rows=4, cols=2)

        self.sina_url_label = wx.StaticText(self, label='sina_url (e.g. http://blog.sina.com.cn/twoclod)')
        self.sina_url_value = wx.TextCtrl(self)

        self.wordpress_admin_label = wx.StaticText(self, label='wordpress_admin: (e.g. admin)')
        self.wordpress_admin_value = wx.TextCtrl(self)

        self.wordpress_url_label = wx.StaticText(self, label='wordpress_url: (e.g. http://huxuan.org/)')
        self.wordpress_url_value = wx.TextCtrl(self)

        self.help_button = wx.Button(self, label=u'帮助(help)')
        self.run_button = wx.Button(self, label=u"运行(run)")

        mainSizer.Add(self.sina_url_label)
        mainSizer.Add(self.sina_url_value)

        mainSizer.Add(self.wordpress_admin_label)
        mainSizer.Add(self.wordpress_admin_value)

        mainSizer.Add(self.wordpress_url_label)
        mainSizer.Add(self.wordpress_url_value)

        mainSizer.Add(self.help_button)
        mainSizer.Add(self.run_button)

        self.Bind(wx.EVT_BUTTON, self.help_show, self.help_button)
        self.Bind(wx.EVT_BUTTON, self.call_core, self.run_button)

        self.SetSizerAndFit(mainSizer)
        self.Show(True)

    def call_core(self, event):
        """Call the core convert process
        """
        args = [self.sina_url_value.GetValue(),
                self.wordpress_admin_value.GetValue(),
                self.wordpress_url_value.GetValue(), ]
        Sina2WordPressCore(self, *args)

    def progress_init(self, msg):
        """docstring for progress_init"""
        self.progressDialog = wx.ProgressDialog('Sina2WordPress Progress', msg)
        self.progressDialog.SetSize((640, 100))

    def progress_update(self, msg, count=0, total=1):
        """docstring for progress_update"""
        self.progressDialog.Update(99 * count / total, msg)

    def finish_show(self, msg):
        """docstring for finish_show"""
        finishDialog = Sina2WordPressMessageDialog(self.progressDialog, msg, 'Sina2WordPress Finish', wx.OK)
        self.progressDialog.Destroy()
        self.Close(True)

    def help_show(self, event):
        """Show help info dialog
        """
        content = 'http://github.com/huxuan/sina2wordpress'
        helpDialog = Sina2WordPressMessageDialog(self, content, 'Help', wx.OK)

class Sina2WordPressMessageDialog(wx.MessageDialog):
    """MessageDialog class for Sinaw2WordPress
    """
    def __init__(self, *args, **kwargs):
        """Init Sina2WordPressMessageDialog"""
        super(Sina2WordPressMessageDialog, self).__init__(*args, **kwargs)
        self.ShowModal()
        self.Destroy()
