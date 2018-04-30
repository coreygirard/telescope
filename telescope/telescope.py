from collections import namedtuple
import foldr2 as foldr


Node = namedtuple('Node', 'type val args kwargs')

def convert_tree(tree):
    if isinstance(tree, str):
        return {tree: None}

    d = {}
    for k, v in tree:
        if k.startswith('.'):
            k = k.lstrip('.')
            if k.endswith('()'):
                k = k[:-2]
                d[k] = {'()': None}
            elif k.endswith('[]'):
                k = k[:-2]
                d[k] = {'[]': None}
            elif v == []:
                d[k] = None
            else:
                d[k] = convert_tree(v)

        elif k[0]+k[-1] == '{}':
            return k

    return d


def merge_tree(tree, ref):
    # fills in {links}

    d = {}
    for k, v in tree.items():
        if v is None:
            d[k] = v
        elif isinstance(v, dict):
            d[k] = merge_tree(v, ref)
        elif v[0]+v[-1] == '{}':
            d[k] = ref[v[1:-1]]
        else:
            d[k] = v

    return d


def build_tree(filename):
    """Builds Telescope tree structure from YML file

    Reads YML file and parses it into a virtual object hierarchy

    Args:
        filename: A relative filepath to a valid YML file
            specifying a Telescope tree structure

    Returns:
        A dict corresponding to the abstract structure of the desired
        Telescope behavior. Values of this dict may be nested dicts.
        For example:

        {'()': None,
         '[]': {42: {'()':None}},
         '.':  {'bbb1':None,
                'bbb2':{'()':None}}}
    """

    # read file line-by-line, stripping whitespace from right
    # and ignoring blank lines
    with open(filename, 'r') as file:
        data = [line.rstrip() for line in file if line.rstrip() != '']

    # build a list of (line_indent, stripped_line) tuples for each line
    data = [(len(line)-len(line.lstrip()), line.lstrip()) for line in data]

    head = data[0][1]

    d = {}
    for k, v in foldr.from_list(data, simple=True):
        d[k] = v

    for k, v in d.items():
        d[k] = convert_tree(v)
    d = merge_tree(d, d)
    return d[head]

class Telescope(object):
    def __init__(self, d, path=None):
        if isinstance(d, str):
            self.d = build_tree(d)
        else:
            self.d = d

        if path is None:
            self.path = []
        else:
            self.path = path

    def __getattr__(self, k):
        if k == 'handle':
            return self.__getattribute__(k)

        #print(k, self.d.keys())

        print(k, self.d.keys())
        if k not in self.d.keys():
            raise AttributeError(k)

        new_path = self.path+[Node(type='attr',
                                   val=k,
                                   args=None,
                                   kwargs=None)]
        if self.d[k] is None:
            return self.handle(new_path)
        # else:
        return Telescope(self.d[k],
                         self.callback,
                         new_path)

    def _nonattr(self, kind, args, kwargs):
        try:
            temp_val = self.path.pop().val
        except:
            temp_val = None

        new_path = self.path+[Node(type=kind,
                                   val=temp_val,
                                   args=args,
                                   kwargs=kwargs)]

        if self.d[kind] is None:
            return self.handle(new_path)
        # else:
        return Telescope(self.d[kind],
                         self.callback,
                         new_path)

    def __getitem__(self, k):
        if '[]' not in self.d.keys():
            raise TypeError('object does not support indexing')

        return self._nonattr('[]', k, None)

    def __call__(self, *args, **kwargs):
        if '()' not in self.d.keys():
            raise TypeError('object is not callable')

        return self._nonattr('()', args, kwargs)

    def __dir__(self):
        # TODO: return actual useful functionality
        return sorted(list(self.d.keys()))


class Tele(object):
    def __init__(self, *args, **kwargs):
        self._telescope = Telescope(self.tree)

    def __getattr__(self, k):
        return getattr(self._telescope, k)


def telescope(tree):
    temp = Tele
    temp.tree = tree
    return temp
