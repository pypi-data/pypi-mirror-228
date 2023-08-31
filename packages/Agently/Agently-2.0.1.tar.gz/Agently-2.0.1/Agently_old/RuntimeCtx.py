class RuntimeCtx(object):
    def __init__ (self, father = None, init_data = {}):
        self.father = father
        self.runtime_ctx_data = init_data
        return

    def set (self, domain, key, value):
        if domain not in self.runtime_ctx_data:
            self.runtime_ctx_data.update({ domain: {} })
        self.runtime_ctx_data[domain].update({ key: value })
        return

    def add (self, domain, key, value):
        if domain not in self.runtime_ctx_data:
            self.runtime_ctx_data.update({ domain: {} })
        if key in self.runtime_ctx_data[domain]:
            if not isinstance(self.runtime_ctx_data[domain][key], set):
                if isinstance(self.runtime_ctx_data[domain][key], list):
                    self.runtime_ctx_data[domain][key] = set(self.runtime_ctx_data[domain][key])
                    self.runtime_ctx_data[domain][key].add(value)
                else:
                    self.runtime_ctx_data[domain].update({ key: value })
            else:
                self.runtime_ctx_data[domain][key].add(value)

    def get (self, domain, key):
        if domain in self.runtime_ctx_data and key in self.runtime_ctx_data[domain]:
            return self.runtime_ctx_data[domain][key]
        else:
            return None if self.father == None else self.father.runtime_ctx.get(domain, key)

    def set_all (self, runtime_ctx_data):
        self.runtime_ctx_data = runtime_ctx_data
        return

    def get_all (self):
        return self.runtime_ctx_data