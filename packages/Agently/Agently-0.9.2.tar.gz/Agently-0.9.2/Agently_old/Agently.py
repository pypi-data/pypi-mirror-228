from .RuntimeCtx import RuntimeCtx
from .WorkNode import WorkNode

class Agently(object):
    def __init__ (self, options = {}):
        self.runtime_ctx = RuntimeCtx(None, { "options": options })
        return