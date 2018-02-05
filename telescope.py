class Telescope(object):
    def __init__(self,d,callback,path=[]):
        self.d = d
        self.callback = callback
        self.path = path

    def __getattr__(self,k):
        if type(self.d) != dict:
            raise Exception('something')

        if k not in self.d.keys():
            raise AttributeError(k)

        if k in self.d.keys():
            return Telescope(self.d[k],
                             self.callback,
                             self.path+[k])

    def __call__(self,*args,**kwargs):
        if self.d != '()':
            raise TypeError('object is not callable')
        return self.callback(self.path,*args,**kwargs)
