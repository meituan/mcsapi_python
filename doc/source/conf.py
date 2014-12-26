# -*- coding: utf-8 -*-

import sys
import os

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'美团云MOS Python SDK及客户端'
copyright = u'2013, Qiu Jian'

version = '0.1'
release = '20131014'

language = 'zh_CN'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

html_use_index = False

html_split_index = False

html_show_sourcelink = False

htmlhelp_basename = 'mosapi_python_sdkdoc'
