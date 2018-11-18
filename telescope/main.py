class Telescope(object):
    def __init__(self, chain, structure, mode, callback):
        self.chain = chain
        self.structure = structure
        self.mode = mode
        self.callback = callback

    def __getattr__(self, e):
        if e not in self.structure:
            raise AttributeError()

        _type, child = self.structure[e]
        if _type == "" and child is None:
            return self.callback(self.chain + [(e, None, None)])

        return Telescope(self.chain + [e], child, _type, self.callback)

    def __repr__(self):
        return f"Telescope(chain={self.chain},\n          structure={self.structure},\n          mode={self.mode})"

    def __call__(self, *args, **kwargs):
        if self.mode != "()":
            raise AttributeError()

        chain = self.chain[:-1] + [(self.chain[-1] + "()", args, kwargs)]
        if self.structure is None:
            return self.callback(chain)
        else:
            return Telescope(chain, self.structure, "", self.callback)

    def __getitem__(self, k):
        if self.mode != "[]":
            raise AttributeError()

        chain = self.chain[:-1] + [(self.chain[-1] + "[]", k, None)]
        if self.structure is None:
            return self.callback(chain)
        else:
            return Telescope(chain, self.structure, "", self.callback)
