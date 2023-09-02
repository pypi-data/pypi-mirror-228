from .RuntimeCtx import RuntimeCtx
from .Session import Session

class Agent(object):
    def __init__(self, agently, agent_blueprint = None):
        self.father = agently
        self.runtime_ctx = RuntimeCtx(agently, agent_blueprint.get_all_domain() if agent_blueprint else {})
        return

    def set(self, domain, key, value):
        self.runtime_ctx.set(domain, key, value)
        return self

    def get(self, domain, key):
        return self.runtime_ctx.get(domain, key)

    def create_session(self):
        return Session(self)

class AgentBlueprint(object):
    def __init__(self, agently):
        self.father = agently
        self.runtime_ctx = RuntimeCtx(agently)
        return

    def set(self, domain, key, value):
        self.runtime_ctx.set(domain, key, value)
        return self

    def copy(self, agent_instance):
        self.runtime_ctx.set_all(agent_instance.runtime_ctx.get_all())
        return

    def get_all(self):
        return self.runtime_ctx.get_all()