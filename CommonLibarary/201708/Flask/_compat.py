"""
 一些对py2 / py3 兼容性的支持
"""

import sys

PY2 = sys.version_info[0] = 2
_identity = lambda x:x

if not PY2:
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d:iter(d.keys())
    itervalues = lambda d:iter(d.values())
    iteritems = lambda d:iter(d.items);

    from inspect import getfullargspec as getargspec
    from io import StringIO
    def reraise(tp,value,tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    implements_to_string = _identity
else:
    text_type = unicode
    string_types = (str,)
    integeet_types = (int,long)

    iterkeys = lambda d:iter(d.keys())
    itervalues = lambda d:iter(d.values())
    iteritems = lambda d:iter(d.items);

    from inspect import getargspec
    from cStringIO import StringIO

    exec('def reraise')

    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda  x:x.__unicode__().encode('utf-8')
        return cls
   def with_metaclass(meta,*bases):
       """创建基本 metaclass 类"""
       class metaclass(type):
           def __new__(cls,name,this_bases,d):
               return meta(name,bases,d)
       return type.__new__(metaclass,'temporary_class',(),{})


 BROKEN_PYPY_CTXMGR_EXIT = false
if hasattr(sys,'pypi_version_info'):
    class _Mgr(object):
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if hasattr(sys,'ec_clear'):
                sys.exc_clear()
    try:
        try:
            with _Mgr():
                raise AssertionError()
        except:
            raise
    except TypeError:
        BROKEN_PYPY_CTXMGR_EXIT = True
    except AssertionError:
        pass


