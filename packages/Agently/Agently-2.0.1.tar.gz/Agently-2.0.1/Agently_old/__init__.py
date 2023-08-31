from .RuntimeCtx import RuntimeCtx
from .Agent import Agent, AgentBlueprint

class Agently(object):
    def __init__ (self, options = {}):
        self.runtime_ctx = RuntimeCtx(None, { "options": options })
        return

    def create_agent (self, agent_blueprint = None):
        return Agent(self, agent_blueprint)

    def create_blueprint (self):
        return AgentBlueprint(self)

    def create_func (self):
        return 

    def set(domain, key, value):
        self.runtime_ctx.set(domain, key, value)
        return

    def get(domain, key):
        return self.runtime_ctx.get(domain, key)