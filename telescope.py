from pprint import pprint
import sys
sys.path.append("/Users/coreygirard/Documents/GitHub/foldr")
import foldr

spine_properties = {'visible':{'()':None},
                    'bounds':{'()':None},
                    'ticks':{'.':{'major':{'()':None},
                                  'minor':{'()':None}}}}
tree = {'.':{'plot':{'()':None},
             'scatter':{'()':None},
             'xlim':{'()':None},
             'ylim':{'()':None},
             'line':{'.':{'label':{'()':None}}},
             'spine':{'.':{'left':{'.':spine_properties},
                           'right':{'.':spine_properties},
                           'top':{'.':spine_properties},
                           'bottom':{'.':spine_properties}}}}}

def convert_tree(tree):
    if type(tree) == str:
        if tree.endswith('()'):
            return {'()':None}

    d = {}
    for k,v in tree:
        if k.startswith('.'):
            if '.' not in d:
                d['.'] = {}

            k = k[1:]
            if k.endswith('()'):
                k = k[:-2]
                d['.'][k] = {'()':None}
            elif k.endswith('[]'):
                k = k[:-2]
                d['.'][k] = {'[]':None}
            else:
                d['.'][k] = convert_tree(v)

        elif k[0]+k[-1] == '{}':
            return k

    return d

def merge_tree(tree,ref):
    d = {}
    for k,v in tree.items():
        if v == None:
            d[k] = v
        elif type(v) == dict:
            d[k] = merge_tree(v,ref)
        elif v[0]+v[-1] == '{}':
            d[k] = ref[v[1:-1]]
        else:
            d[k] = v

    return d


def build_tree(filename):
    with open(filename,'r') as f:
        data = [line.rstrip() for line in f if line.rstrip() != '']

    data = [(len(line)-len(line.lstrip()),line.lstrip()) for line in data]

    d = {}
    for k,v in foldr.fromList(data,simple=True):
        d[k] = v

    for k,v in d.items():
        d[k] = convert_tree(v)
    d = merge_tree(d,d)
    return d

class Telescope(object):
    def __init__(self,d,callback,path=[],k=None):
        if type(d) == str:
            self.d = build_tree(d)[k]
        else:
            self.d = d
        self.callback = callback
        self.path = path

    def __getitem__(self,k):
        if '[]' not in self.d.keys():
            raise TypeError('object is not callable')

        new_path = self.path+[('[]',)]
        return self.callback(new_path,k,{})

        '''
        if type(self.d) != dict:
            raise Exception('something')
        if '[]' not in self.d.keys():
            raise Exception('something')
        if k not in self.d['[]'].keys():
            raise AttributeError('[]'+str(k))

        new_path = self.path+[('[]',k)]
        if self.d['[]'][k] == None:
            return self.callback(new_path)
        else:
            return Telescope(self.d['[]'][k],
                             self.callback,
                             new_path)
        '''

    def __getattr__(self,k):
        if type(self.d) != dict:
            raise Exception('something')
        if '.' not in self.d.keys():
            raise Exception('something')
        if k not in self.d['.'].keys():
            raise AttributeError(str(self.d['.'].keys()))
            #raise AttributeError('.'+str(k))

        new_path = self.path+[('.',k)]
        if self.d['.'][k] == None:
            return self.callback(new_path)
        else:
            return Telescope(self.d['.'][k],
                             self.callback,
                             new_path)

    def __call__(self,*args,**kwargs):
        if '()' not in self.d.keys():
            raise TypeError('object is not callable')

        new_path = self.path+[('()',)]
        return self.callback(new_path,*args,**kwargs)
