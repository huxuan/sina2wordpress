#!/usr/bin/python
#encoding: utf8
# +-----------------------------------------------------------------------------
# | File: Sina2WordPress.py
# | Author: huxuan
# | E-mail: i(at)huxuan.org
# | Created: 2012-12-11
# | Last modified: 2012-02-24
# | Description:
# |     Main Process of Sina2WordPress
# |
# | Copyrgiht (c) 2012 by huxuan. All rights reserved.
# | License GPLv3
# +-----------------------------------------------------------------------------

import sys
import time

import wx

import Sina2WordPressCore

SLEEP_TIME = 2

class Sina2WordPress():
    """Summary of Sina2WordPress
    """
    def __init__(self, sina_url, wordpress_admin, wordpress_url):
        """Init Sina2WordPress"""
        self.output_file = wordpress_admin + '.xml'
        f = file(self.output_file, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<rss version="2.0"\n\txmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"\n\txmlns:content="http://purl.org/rss/1.0/modules/content/"\n\txmlns:wfw="http://wellformedweb.org/CommentAPI/"\n\txmlns:dc="http://purl.org/dc/elements/1.1/"\n\txmlns:wp="http://wordpress.org/export/1.1/"\n>\n\n<channel>\n<wp:wxr_version>1.1</wp:wxr_version>\n')
        f.close()

        print sina_url
        content_url, sina_admin = Sina2WordPressCore.indexAnalyze(sina_url)
        
        posts_urls = []
        while True:
            print content_url
            time.sleep(SLEEP_TIME / 2)

            posts_page_urls, content_url = Sina2WordPressCore.contentAnalyze(content_url) 
            posts_urls.extend(posts_page_urls)
            if not content_url:
                break
        posts_urls.reverse()

        comment_id = 0
        for post_url in posts_urls[4:]:
            time.sleep(SLEEP_TIME)
            #Todo(huxuan): Show post Progress here
            print '(%d/%d)' % (posts_urls.index(post_url) + 1, len(posts_urls)) ,post_url
            post_text, comment_status = Sina2WordPressCore.postAnalyze(post_url, wordpress_admin)
            text = [post_text]

            if comment_status == 'open': 
                key = post_url.replace(r'http://blog.sina.com.cn/s/blog_','').replace(r'.html','')
                num = 0

                while True:
                    time.sleep(SLEEP_TIME)

                    num += 1
                    comment_url = r'http://blog.sina.com.cn/s/comment_%s_%d.html' %(key, num)
                    print comment_url

                    comment_text, comment_id = Sina2WordPressCore.commentAnalyze(
                            comment_url, comment_id, sina_admin, wordpress_admin, wordpress_url)

                    if comment_text:
                        text.append(comment_text)
                    else:
                        break

            text.append('\n</item>')
            self.output(''.join(text))

        self.output('\n</channel>\n</rss>')

        print 'Succeed !'
    
    def output(self, text):
        """docstring for print2file"""
        f = file(self.output_file, 'a')
        f.write(text)
        f.close()

class Sina2WordPressInterface(object):
    """Virtual Interface for Sina2WordPress
    """
    def __init__(self, *args):
        """Init Sina2WordPressGUI"""
        pass

    def ShowProgress(self, *args, **kwargs):
        """docstring for ShowProgress"""
        pass

    def ShowError(self, msg):
        """Summary of ShowError
        """
        pass

class Sina2WordPressCLI(Sina2WordPressInterface):
    """Command Line Interface for Sina2WordPress
    """
    def __init__(self, *args):
        """Init Sina2WordPressGUI"""
        Sina2WordPress(*args)

    def ShowProgress(self, *args, **kwargs):
        """docstring for ShowProgress"""
        pass

    def ShowError(self, msg):
        """Summary of ShowError
        """
        pass

class Sina2WordPressGUI(Sina2WordPressInterface):
    """Graphic User Interface for Sina2WordPress
    """
    def __init__(self, *args):
        """Init Sina2WordPressGUI"""
        self.app = wx.App()
        self.window = Sina2WordPressWindow(None, title='Sina2WordPress')
        self.app.MainLoop()

    def ShowProgress(self, *args, **kwargs):
        """docstring for ShowProgress"""
        pass

    def ShowError(self, msg):
        """Summary of ShowError
        """
        pass

class Sina2WordPressWindow(wx.Frame):
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

        self.help_button = wx.Button(self, label='帮助(help)')
        self.run_button = wx.Button(self, label="运行(run)")

        mainSizer.Add(self.sina_url_label)
        mainSizer.Add(self.sina_url_value)

        mainSizer.Add(self.wordpress_admin_label)
        mainSizer.Add(self.wordpress_admin_value)

        mainSizer.Add(self.wordpress_url_label)
        mainSizer.Add(self.wordpress_url_value)

        mainSizer.Add(self.help_button)
        mainSizer.Add(self.run_button)

        self.Bind(wx.EVT_BUTTON, self.ShowHelp, self.help_button)
        self.Bind(wx.EVT_BUTTON, self.CallCore, self.run_button)

        self.SetSizerAndFit(mainSizer)
        self.Show(True)

    def CallCore(self, event):
        """Call the core convert process
        """
        args = [self.sina_url_value.GetValue(),
                self.wordpress_admin_value.GetValue(),
                self.wordpress_url_value.GetValue(), ]
        Sina2WordPress(*args)
        self.Close(True)

    def ShowHelp(self, event):
        """Show help info dialog
        """
        content = 'http://github.com/huxuan/sina2wordpress'
        helpDialog = Sina2WordPressMessageDialog(self, content, 'Help', wx.OK)

class Sina2WordPressMessageDialog(wx.MessageDialog):
    """MessageDialog of Sinaw2WordPress
    """
    def __init__(self, *args, **kwargs):
        """Init Sina2WordPressMessageDialog"""
        super(Sina2WordPressMessageDialog, self).__init__(*args, **kwargs)
        self.ShowModal()
        self.Destroy()

def main():
    """Summary of main
    """
    if len(sys.argv) == 4:
        Sina2WordPressCLI(*sys.argv[1:4])
    elif len(sys.argv) == 1:
        Sina2WordPressGUI()
    else:
        print '[Error] The number of parameters is invalid! 4 Needed.'

if __name__ == '__main__':
    main()
