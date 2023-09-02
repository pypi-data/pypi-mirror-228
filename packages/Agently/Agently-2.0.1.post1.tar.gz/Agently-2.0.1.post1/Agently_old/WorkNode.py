class WorkNodeManage(object):
    def __init__(self, work_node):
        self.worknodes = work_node.worknodes

class WorkNode(object):
    def __init__(self, agently):
        self.agently = agently
        self.worknodes = {}
        self.Manage = WorkNodeManage(self, )
        return

    async def run(work_node_name):
        if work_node_name in self.worknodes:
            
        else:
            return { ok: False, message: f"No worknodes named:{ work_node_name }" }