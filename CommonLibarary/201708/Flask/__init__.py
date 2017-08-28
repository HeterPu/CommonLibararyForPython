# -*- 编码:utf-8 -*-
"""
flask
一个基于WerkZeng的微框架,并继承了一些很好的实战模块
版权 Armin Ronache
"""

__version__ = '0.13-dev'
from werkzeug.exceptions import  abort
from werkzeug.utils import redirect
from jinja2 import Markup,escape

from . import json
