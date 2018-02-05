from pprint import pprint

class Telescope(object):
    def __init__(self,d,callback,path=[]):
        self.d = d
        self.callback = callback
        self.path = path

    def __getitem__(self,k):
        if type(self.d) != dict:
            raise Exception('something')
        if '[]' not in self.d.keys():
            raise Exception('something')
        if k not in self.d['[]'].keys():
            raise AttributeError('[]'+str(k))

        return Telescope(self.d['[]'][k],
                         self.callback,
                         self.path+['[]'+str(k)])


    def __getattr__(self,k):
        if type(self.d) != dict:
            raise Exception('something')
        if '.' not in self.d.keys():
            raise Exception('something')
        if k not in self.d['.'].keys():
            raise AttributeError('.'+str(k))

        return Telescope(self.d['.'][k],
                         self.callback,
                         self.path+['.'+str(k)])

    def __call__(self,*args,**kwargs):
        #pprint(self.d,width=15)

        if '()' not in self.d.keys():
            raise TypeError('object is not callable')

        return self.callback(self.path,*args,**kwargs)