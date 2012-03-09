#!/usr/bin/python
#encoding: utf8
# +-----------------------------------------------------------------------------
# | File: Sina2WordPressCore.py
# | Author: huxuan
# | E-mail: i(at)huxuan.org
# | Created: 2011-02-21
# | Last modified: 2012-03-08
# | Description:
# |     Core Process of Sina2WordPress
# |     Analyze Sina Blog and convert it to WXR for WordPress
# |
# | Copyrgiht (c) 2012 by huxuan. All rights reserved.
# | License GPLv3
# +-----------------------------------------------------------------------------

import re
import json
import time
import urllib
import urllib2
import cookielib

SLEEP_TIME = 2

headers = {'Referer':'http://blog.sina.com.cn/', 'User-Agent':'Opera/9.60',}

sina_admin_pattern = re.compile(r'<title>(.*?)_新浪博客</title>')
contents_pattern = re.compile(r'<a +href="(.*?)">博文目录</a>')
post_pattern = re.compile(r'<a +title.*?href="(.*?)">.*?</a>')
nextpage_pattern = re.compile(r'<li class="SG_pgnext"><a href="(.*?)".*</li>')
post_title_pattern = re.compile(r'<h2.*?titName SG_txta">(.*?)</h2>')
post_time_pattern = re.compile(r'<span class="time SG_txtc">[(](.*?)[)]</span>')
post_content_pattern = re.compile(r'<!-- 正文开始 -->(.*?)(<INS>|<!-- 正文结束 -->)', re.S)
content_replace_pattern = re.compile(r'<wbr>|<span class=\'MASSf21674ffeef7\'>.*?</span>|<p STYLE="TexT-inDenT: 2em">&nbsp;<wbr></P>|<div>&nbsp;<wbr></DIV>| STYLE="TexT-inDenT: 2em"|<div id="sina_keyword_ad_area2" class="articalContent  ">', re.S)
content_space_replace_pattern = re.compile(r'&nbsp;')
post_category_pattern = re.compile(r'<span class="SG_txtb">分类：</span>.*?<a.*?>(.*?)</a>', re.S)
post_tags_pattern = re.compile(r'\$tag=\'(.*?)\'')
comment_author_pattern = re.compile(r'<span class="SG_revert_Tit".*?>(.*?)</span>')
comment_url_pattern = re.compile(r'<a href="(.*?)" target="_blank">(.*?)</a>')
comment_time_pattern = re.compile(r'<em class="SG_txtc">(.*?)</em>')
comment_content_pattern = re.compile(r'(?:<div class="SG_revert_Inner SG_txtb".*?>|<p class="myReInfo wordwrap">)(.*?)</div>', re.S)

class Sina2WordPressCore():
    """Summary of Sina2WordPressCore
    """
    def __init__(self, interface, sina_url, wordpress_admin, wordpress_url):
        """Init Sina2WordPress"""
        self.output_file = wordpress_admin + '.xml'
        f = file(self.output_file, 'w')
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<rss version="2.0"\nxmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"\nxmlns:content="http://purl.org/rss/1.0/modules/content/"\nxmlns:wfw="http://wellformedweb.org/CommentAPI/"\nxmlns:dc="http://purl.org/dc/elements/1.1/"\nxmlns:wp="http://wordpress.org/export/1.1/"\n>\n\n<channel>\n<wp:wxr_version>1.1</wp:wxr_version>\n')
        f.close()

        msg = 'Begin to Convert: %s' % (sina_url, )
        interface.ProgressInit(msg)
        content_url, sina_admin = index_analyze(sina_url)
        
        posts_urls = []
        while True:
            time.sleep(SLEEP_TIME / 2)

            msg = 'Analyzing Contents: %s' % content_url
            interface.ProgressUpdate(msg)
            posts_page_urls, content_url = content_analyze(content_url) 
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
            post_text, comment_status = post_analyze(post_url, wordpress_admin)
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

                    comment_text, comment_id = comment_analyze(
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

def urlopen_request(req):
    """docstring for urlopen_request"""
    try:
        res = urllib2.urlopen(req).read()
    except:
        time_sleep = 30
        while True:
            print 'Fuck for exception sleep!', time_sleep
            time.sleep(time_sleep)
            try:
                res = urllib2.urlopen(req).read()
                break
            except:
                time_sleep += 30
                pass
    return res

def comment_analyze(url, comment_id, sina_admin, wordpress_admin,wordpress_url):
    """Analyze the comment page via json.loads() and regular expression"""

    #headers['Referer'] = url
    request = urllib2.Request(url, None, headers)
    page = urlopen_request(request).replace('data:','\"data\":',1)

    if 'noCommdate' in page:
        return None, comment_id
    
    data = json.loads(page)['data']
    author = comment_author_pattern.findall(data)
    comment_time = comment_time_pattern.findall(data)
    content = comment_content_pattern.findall(data)
    text = []
    for i in range(len(author)):
        parent = 0
        url = ''
        if author[i] == u'博主回复：' or sina_admin in author[i]:
            parent = comment_id
            author[i] = wordpress_admin
            url = wordpress_url
        else:
            result = comment_url_pattern.search(author[i])
            if result:
                url = result.group(1)
                author[i] = result.group(2)
        comment_id += 1
        content[i] = content_replace_pattern.sub('', content[i])
        content[i] = content_space_replace_pattern.sub(' ', content[i])
        text.append('\n<wp:comment>\n<wp:comment_id>'+str(comment_id)+'</wp:comment_id>\n<wp:comment_author><![CDATA['+author[i].encode('utf8')+']]></wp:comment_author>\n<wp:comment_author_url>'+url.encode('utf8')+'</wp:comment_author_url>\n<wp:comment_date>'+comment_time[i].encode('utf8')+'</wp:comment_date>\n<wp:comment_content><![CDATA['+content[i].encode('utf8')+']]></wp:comment_content>\n<wp:comment_approved>1</wp:comment_approved>\n<wp:comment_parent>'+str(parent)+'</wp:comment_parent>\n</wp:comment>')

    return ''.join(text), comment_id

def post_analyze(url, wordpress_admin):
    """Analyze the post page to get almost all information needed
    except for comments which will be done in another function"""

    request = urllib2.Request(url, None, headers)
    page = urlopen_request(request)
    #headers['Referer'] = url

    post_title = post_title_pattern.search(page).group(1)
    post_time = post_time_pattern.search(page).group(1)
    post_content = post_content_pattern.search(page).group(1)
    post_content = content_replace_pattern.sub('', post_content)
    post_content = content_space_replace_pattern.sub(' ', post_content)
    post_content = post_content.lstrip().rstrip()
    if post_content[-6:] == '</div>': 
        post_content = post_content[:-6].rstrip()

    result = post_category_pattern.search(page)
    if result:
        post_category = result.group(1)
    else: 
        post_category = 'Uncategorized'

    if r'<div class="allComm">' in page:
        comment = 'open'
    else:
        comment = 'closed'

    text = ['\n<item>\n<title>'+post_title+'</title>\n<dc:creator>' + str(wordpress_admin) + '</dc:creator>\n<content:encoded><![CDATA['+post_content+']]></content:encoded>\n<wp:post_date>'+post_time+'</wp:post_date>\n<wp:comment_status>'+comment+'</wp:comment_status>\n<wp:status>publish</wp:status>\n<wp:post_type>post</wp:post_type>\n<wp:is_sticky>0</wp:is_sticky>\n<category domain="category" nicename="'+urllib.quote(post_category)+'"><![CDATA['+post_category+']]></category>']

    result = post_tags_pattern.search(page)
    if result: 
        post_tags = result.group(1)
        for tag in post_tags.split(','):
            text.append('\n<category domain="post_tag" nicename="'+urllib.quote(tag)+'"><![CDATA['+tag+']]></category>')
    
    return ''.join(text), comment

def content_analyze(url):
    """Analyze the contents to collect the urls of all posts"""
    request = urllib2.Request(url, None, headers)
    page = urlopen_request(request)
    posts_urls = post_pattern.findall(page)
    nextpage_result = nextpage_pattern.search(page)
    if nextpage_result:
        #headers['Referer'] = url
        nextpage_url = nextpage_result.group(1)
    else:
        nextpage_url = None
    return posts_urls, nextpage_url 

def index_analyze(url):
    """Analyze the index to find out the url of the contents"""
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    #headers['Referer'] = url
    request = urllib2.Request(url, None, headers)
    page = urlopen_request(request)
    sina_admin = sina_admin_pattern.search(page).group(1).decode('utf8')
    content_url = contents_pattern.search(page).group(1)

    return content_url, sina_admin
