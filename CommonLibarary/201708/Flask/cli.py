from __future__ import print_function

import ast
import inspect
import os
import re
import sys
import traceback
from functools import update_wrapper
from operator import  attrgetter
from threading import Lock,Thread

import click
from . import __version__
from ._compat import
from .globals import
from .helpers import
try:
    import dotenv
except ImportError:
    DOTENV = None

class NoAppException(click.UsageError):
    """当应用没有找到或未加载就会报错
    """
def find_best_app(script_info,module):
    """给一个模块实例并且尝试去寻找模块中最好的应用或者报错"""
    from . import Flask
    # 首先寻找最相似的名字
    for attr_name in ('app','application'):
        app = getattr(module,attr_name,None)
        if isinstance(app,Flask):
            return app

    # 否则寻找仅仅是flask实例的对象
    matches = [v for k,v in iter]