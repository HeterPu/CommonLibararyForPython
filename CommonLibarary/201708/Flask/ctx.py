import sys
from functools import update_wrapper
from werkzeug.exceptions import HTTPException
from .globals import _request_ctx_stack,_app_ctx_stack
from .signals import appcontext_pushed,appcontext_popped
from ._compat import BROKEN_PYPY_CTXMGR_EXIT

_sentinel = object()

class _AppCtxGlobals(object):
    """a plain object."""

    def get(self,name,default=None):
        return self.__dict__.get(name,default)

    def pop(self,name,default=_sentinel):
        if default is _sentinel:
            return self.__dict__.pop(name)
        else:
            return self.__dict__.pop(name,default)

    def setdefault(self,name,default=None):
        return self.__dict__.setdefault(name,default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        top = _app_ctx_stack.top
        if top is not None:
            return '<flask.g of %r>' % top.app.name
        return object.__repr__(self)

def after_this_request(f):
    _request_ctx_stack.top._after_request_function.append(f)
    return f

def copy_current_request_context(f):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('this decorator')
    reqctx = top.copy()
    def wrapper(*args,**kwargs)
        with reqctx:
            return f(*args,**kwargs)
    return update_wrapper(wrapper,f)

def has_request_context():
    return _request_ctx_stack.top is not None

def has_app_context():
    return _app_ctx_stack.top is not None

class AppContext(object):
    def __init__(self,app):
        self.app = app
        self.ur_adapter = app.create_url_adapter(None)
        self.g = app.app_ctx_globals_class()
        self._refcnt = 0
    def push(self):
        self._refcnt += 1
        if hasattr(sys,'exc_clear'):
            sys.exc_clear()
        _app_ctx_stack.push(self)
        appcontext_pushed.send(self.app)
    def pop(self,exc=_sentinel):
        try:
            self._refcnt -= 1
            if self._refcnt <= 0:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                self.app.do_teardown_appcontext(exc)
        finally:
            rv = _app_ctx_stack.pop()
        assert rv is self,'popped %r instead %r' % (rv,self)
        appcontext_popped.send(self.app)
