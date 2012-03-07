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

import Sina2WordPressCore

SLEEP_TIME = 2

class Sina2WordPress():
    """Summary of Sina2WordPress
    """
    def __init__(self, interface, sina_url, wordpress_admin, wordpress_url):
        """Init Sina2WordPress"""
        self.output_file = wordpress_admin + '.xml'
        f = file(self.output_file, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<rss version="2.0"\n\txmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"\n\txmlns:content="http://purl.org/rss/1.0/modules/content/"\n\txmlns:wfw="http://wellformedweb.org/CommentAPI/"\n\txmlns:dc="http://purl.org/dc/elements/1.1/"\n\txmlns:wp="http://wordpress.org/export/1.1/"\n>\n\n<channel>\n<wp:wxr_version>1.1</wp:wxr_version>\n')
        f.close()

        msg = 'Begin to Convert: %s' % (sina_url, )
        interface.ProgressInit(msg)
        content_url, sina_admin = Sina2WordPressCore.index_analyze(sina_url)
        
        posts_urls = []
        while True:
            time.sleep(SLEEP_TIME / 2)

            msg = 'Analyzing Contents: %s' % content_url
            interface.ProgressUpdate(msg)
            posts_page_urls, content_url = Sina2WordPressCore.content_analyze(content_url) 
            posts_urls.extend(posts_page_urls)
            if not content_url:
                break
        posts_urls.reverse()
        total = len(posts_urls)

        msg = '(0/%d) Contents Analyze finish. %d Posts Found!' % (total, total)
        interface.ProgressUpdate(msg)

        comment_id = 0
        for post_url in posts_urls:
            time.sleep(SLEEP_TIME)

            count = posts_urls.index(post_url) + 1
            msg = '(%d/%d) Analyzing Post: %s' % (count, total, post_url, )
            interface.ProgressUpdate(msg, count, total)
            post_text, comment_status = Sina2WordPressCore.post_analyze(post_url, wordpress_admin)
            text = [post_text]

            if comment_status == 'open': 
                key = post_url.replace(r'http://blog.sina.com.cn/s/blog_','').replace(r'.html','')
                num = 0

                while True:
                    time.sleep(SLEEP_TIME)

                    num += 1
                    comment_url = r'http://blog.sina.com.cn/s/comment_%s_%d.html' %(key, num)

                    msg = '(%d/%d) Analyzing Comment: %s' % (count, total, comment_url, )
                    interface.ProgressUpdate(msg, count, total)

                    comment_text, comment_id = Sina2WordPressCore.comment_analyze(
                            comment_url, comment_id, sina_admin, wordpress_admin, wordpress_url)

                    if comment_text:
                        text.append(comment_text)
                    else:
                        break

            text.append('\n</item>')
            self.output(''.join(text))

        self.output('\n</channel>\n</rss>')

        msg = 'Convert Succeed!\nThe result is saved in %s.' % (self.output_file, )
        interface.FinishShow(msg)
    
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

    def ProgressInit(self, *args, **kwargs):
        """docstring for ProgressInit"""
        pass

    def ProgressUpdate(self, *args, **kwargs):
        """docstring for ProgressUpdate"""
        pass

    def FinishShow(self, *args, **kwargs):
        """docstring for FinishShow"""
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
        Sina2WordPress(self, *args)

    def ProgressInit(self, msg):
        """docstring for ProgressInit"""
        print msg

    def ProgressUpdate(self, msg, count=0, total=0):
        """docstring for ProgressUpdate"""
        print msg

    def FinishShow(self, msg):
        """docstring for FinishShow"""
        print msg

    def ShowError(self, msg):
        """Summary of ShowError
        """
        pass

def main():
    """Summary of main
    """
    if len(sys.argv) == 4:
        Sina2WordPressCLI(*sys.argv[1:4])
    elif len(sys.argv) == 1:
        import Sina2WordPressGUI
        Sina2WordPressGUI.Sina2WordPressGUI()
    else:
        print '[Error] The number of parameters is invalid! 4 Needed.'

if __name__ == '__main__':
    main()
