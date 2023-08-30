from .RuntimeCtx import RuntimeCtx
from .Workflow import execute_workflow

class Session(object):
    def __init__(self, agent):
        self.father = agent
        self.runtime_ctx = RuntimeCtx(agent)
        return

    def set (self, domain, key, value):
        self.runtime_ctx.set(domain, key, value)
        return self

    def get (self, domain, key):
        return self.runtime_ctx.get(domain, key)

    async def start (self, workflow_name):
        return await execute_workflow(workflow_name)