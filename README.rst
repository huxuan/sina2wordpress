Sina2WordPress
==============

相关页面
----------
- 项目页面_
- 托管代码_
- 参数说明_
- 使用方法_
- 额外说明_

功能说明
----------
- 一个新浪博客搬家到WordPress的Python脚本
- 通过爬取新浪博客的网页并通过正则转换成WXR类型的xml文件
- Wordpress eXtended Rss (WXR) 是WordPress原生支持的导入文件类型
- 目前仍在开发维护中，版本号1.0

已实现功能
----------
- 转换日志的标题、时间、分类、标签、正文
- 转换评论的作者、链接、时间、正文
- 自动识别博主并转换成指定的名称和超链接
- 将“博主回复”转换为WordPress原生的嵌套回复
- 兼容实现CLI（命令行）和GUI（图形界面）两种交互方法
  CLI模式可以在无wxpython module的环境下运行
- 打包成exe，可供无python环境的windows用户使用
- 过滤冗余的HTML代码
- 详尽的运行日志和进度显示

待实现功能
----------
- 抓取博客内嵌的图片
- 抓取博客内嵌的视频 （暂还未确定实现方式）
- 可以拆分转换后的WXR文件并指定文件大小

待完成杂活
----------
- 代码注释

.. _项目页面: http://huxuan.org/projects/sina2wordpress
.. _托管代码: https://github.com/huxuan/sina2wordpress
.. _参数说明: https://github.com/huxuan/sina2wordpress/wiki/Parameters
.. _使用方法: https://github.com/huxuan/sina2wordpress/wiki/Usage
.. _额外说明: https://github.com/huxuan/sina2wordpress/wiki/ExtraTips
