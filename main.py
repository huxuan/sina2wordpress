#!/usr/bin/env python 
#-*-coding:utf-8-*- 
import re
import json
import urllib
import urllib2

contents_pattern=re.compile(r'<a +href="(.*)">博文目录</a>')
post_pattern=re.compile(r'<a +title.*?href="(.*?)">.*?</a>')
nextpage_pattern=re.compile(r'<li class="SG_pgnext"><a href="(.*?)".*</li>')
title_pattern=re.compile(r'<h2.*?titName SG_txta">(.*?)</h2>')
time_pattern=re.compile(r'<span class="time SG_txtc">[(](.*?)[)]</span>')
content_pattern=re.compile(r'<!-- 正文开始 -->(.*?)(<INS>|<!-- 正文结束 -->)', re.S)
content_replace_pattern=re.compile(r'<span class=\'MASSf21674ffeef7\'>.*?</span>|<p STYLE="TexT-inDenT: 2em">&nbsp;<wbr></P>|<div>&nbsp;<wbr></DIV>| STYLE="TexT-inDenT: 2em"|<div id="sina_keyword_ad_area2" class="articalContent  ">', re.S)
category_pattern=re.compile(r'<span class="SG_txtb">分类：</span>.*?<a.*?>(.*?)</a>', re.S)
tags_pattern=re.compile(r'\$tag=\'(.*?)\'')
comment_author_pattern=re.compile(r'<span class="SG_revert_Tit".*?>(.*?)</span>')
comment_url_pattern=re.compile(r'<a href="(.*?)" target="_blank">(.*?)</a>')
comment_time_pattern=re.compile(r'<em class="SG_txtc">(.*?)</em>')
comment_content_pattern=re.compile(r'(?:<div class="SG_revert_Inner SG_txtb".*?>|<p class="myReInfo wordwrap">)(.*?)</div>', re.S)

admin_name='admin'
admin_url='http://huxuan.org/'

def indexAnalyze(url):
    """Analyze the index to find out the url of the contents"""
    page=urllib2.urlopen(url).read()
    content_url=contents_pattern.search(page).group(1)
    contentAnalyze(content_url)

def contentAnalyze(url):
    """Analyze the contents to collect the urls of all posts"""
    post_urls=[]
    while True:
        page=urllib2.urlopen(url).read()
        post_urls.extend(post_pattern.findall(page))
        nextpage_result=nextpage_pattern.search(page)
        if nextpage_result: url=nextpage_result.group(1)
        else: break
    post_urls.reverse()
    postsAnalyze(post_urls)

def postsAnalyze(urls):
    """Analyze the post page to get almost all information needed
    except for comments which will be done in another function"""
    global post_id
    for url in urls:
        post_id+=1
        page=urllib2.urlopen(url).read()
        title=title_pattern.search(page).group(1) 
        time=time_pattern.search(page).group(1)
        content=content_pattern.search(page).group(1)
        content=content_replace_pattern.sub('',content)
        content=content.lstrip().rstrip()
        if content[-6:]=='</div>': content=content[:-6].rstrip()
        result=category_pattern.search(page)
        if result: category=result.group(1)
        else: category='Uncategorized'
        result=tags_pattern.search(page)
        if result: tags=result.group(1)
        else: tags=''
        if r'<div class="allComm">' in page: comment='open'
        else: comment='closed'
        f.write('<item>\n\t<title>'+title+'</title>\n\t<dc:creator>'+admin_name+'</dc:creator>\n\t<content:encoded><![CDATA['+content+']]></content:encoded>\n\t<wp:post_id>'+str(post_id)+'</wp:post_id>\n\t<wp:post_date>'+time+'</wp:post_date>\n\t<wp:comment_status>'+comment+'</wp:comment_status>\n\t<wp:status>publish</wp:status>\n\t<wp:post_type>post</wp:post_type>\n\t<wp:is_sticky>0</wp:is_sticky>\n\t<category domain="category" nicename="'+urllib.quote(category)+'"><![CDATA['+category+']]></category>\n')
        for tag in tags.split(','):
            f.write('\t<category domain="post_tag" nicename="'+urllib.quote(tag)+'"><![CDATA['+tag+']]></category>\n')
        if comment=='open': commentsAnalyze(url.replace(r'http://blog.sina.com.cn/s/blog_','').replace(r'.html',''))
        f.write('</item>\n')
        print urls.index(url)

def commentsAnalyze(key):
    """Analyze the comment page including decode via json.loads() and regular expression"""
    global comment_id
    num=1
    url=r'http://blog.sina.com.cn/s/comment_%s_%d.html' %(key, num)
    page=urllib2.urlopen(url).read().replace('data:','\"data\":',1)
    while not 'noCommdate' in page:
        data=json.loads(page)['data']
        author=comment_author_pattern.findall(data)
        url=[]
        parent=[]
        time=comment_time_pattern.findall(data)
        content=comment_content_pattern.findall(data)
        print str(num)+':'+str(len(author))+':'+str(len(time))+':'+str(len(content))
        for i in range(len(author)):
            if author[i]==u'博主回复：':
                author[i]=admin_name
                parent.append(str(comment_id))
                url.append(admin_url)
            else: 
                parent.append('0')
                result=comment_url_pattern.search(author[i])
                if result:
                    url.append(result.group(1))
                    author[i]=result.group(2)
                else: url.append('')
            comment_id+=1
            f.write('\t<wp:comment>\n\t\t<wp:comment_id>'+str(comment_id)+'</wp:comment_id>\n\t\t<wp:comment_author><![CDATA['+author[i].encode('utf8')+']]></wp:comment_author>\n\t\t<wp:comment_author_url>'+url[i].encode('utf8')+'</wp:comment_author_url>\n\t\t<wp:comment_date>'+time[i].encode('utf8')+'</wp:comment_date>\n\t\t<wp:comment_content><![CDATA['+content[i].encode('utf8')+']]></wp:comment_content>\n\t\t<wp:comment_approved>1</wp:comment_approved>\n\t\t<wp:comment_parent>'+parent[i]+'</wp:comment_parent>\n\t</wp:comment>\n')
        num+=1
        url=r'http://blog.sina.com.cn/s/comment_%s_%d.html' %(key, num)
        page=urllib2.urlopen(url).read().replace('data:','\"data\":',1)

if __name__=='__main__':
    f=file('sina2wordpress.xml','w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n\n<rss version="2.0"\n\txmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"\n\txmlns:content="http://purl.org/rss/1.0/modules/content/"\n\txmlns:wfw="http://wellformedweb.org/CommentAPI/"\n\txmlns:dc="http://purl.org/dc/elements/1.1/"\n\txmlns:wp="http://wordpress.org/export/1.1/"\n>\n\n<channel>\n<wp:wxr_version>1.1</wp:wxr_version>\n')
    post_id=0
    comment_id=0
    index_url='http://blog.sina.com.cn/victorhu'
    indexAnalyze(index_url)
    f.write('</channel>\n</rss>')
    f.close()
