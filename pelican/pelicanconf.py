#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Nathan Baker'
SITENAME = 'Nathan A. Baker'
SITEURL = ''

PATH = 'content'
TIMEZONE = 'America/Los_Angeles'

INDEX_SAVE_AS = "blog_index.html"

# Flex - nice and simple but doesn't include categories
# lannisport - needs work (background, "blog" label, etc.)
# pelican-bootstrap3 - simple but pretty much ready to be used
# pelican-elegant - pretty blog-centric; would need work to make functional
# pelican-sober - ok but need to rename "blogroll"
THEME = './themes/pelican-bootstrap3'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["tag_cloud"]
TAG_CLOUD_SORTING = "size"
DISPLAY_ARTICLE_INFO_ON_INDEX = True
GOOGLE_ANALYTICS = "UA-11026338-13"
TYPOGRIFY = True

ARTICLE_URL = 'publications/{slug}.html'
ARTICLE_SAVE_AS = 'publications/{slug}.html'

# Blogroll
LINKS = (('Google Scholar', 'https://scholar.google.com/citations?user=L9dwKyUAAAAJ&hl=en'),
    ('ORCID', 'http://orcid.org/0000-0002-5892-6506'),)

# Social widget
SOCIAL = (('LinkedIn', 'http://www.linkedin.com/in/nathanandrewbaker'),
    ("Mendeley", "https://www.mendeley.com/profiles/nathan-baker1/"),)

DEFAULT_PAGINATION = False

FAVICON = "images/favicon.ico"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
