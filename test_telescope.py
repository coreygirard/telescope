import unittest
import doctest
import telescope


class Flytrap(object):
    def __init__(self):
        self.route = None
        self.args = None
        self.kwargs = None

    def f(self, route, *args, **kwargs):
        self.route = route
        self.args = args
        self.kwargs = kwargs


class TestCallableRoot(unittest.TestCase):
    def test_callable_root(self):
        tree = {'()': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele()

        self.assertEqual([flytrap.route,
                          flytrap.args,
                          flytrap.kwargs],
                         [[('()',)],
                          tuple(),
                          {}])


class TestAttribute(unittest.TestCase):
    def test_attribute(self):
        tree = {'.': {'aaa': None}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa

        self.assertEqual([flytrap.route,
                          flytrap.args,
                          flytrap.kwargs],
                         [[('.', 'aaa')],
                          (),
                          {}])

        temp = lambda a: a.bbb
        self.assertRaises(AttributeError, temp, tele)


class TestElement(unittest.TestCase):
    def test_element(self):
        tree = {'[]': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele['abc']

        self.assertEqual([flytrap.route,
                          flytrap.args,
                          flytrap.kwargs],
                         [[('[]',)],
                          ('abc',),
                          {}])

class TestFileLoad(unittest.TestCase):
    def test_file_load(self):
        result = telescope.build_tree('chart.yml')
        expected = {'.': {'bbb': None,
                          'ccc': {'[]': None},
                          'ddd': {'()': None},
                          'eee': {'.': {'jjj': None}}}}
        self.assertEqual(result, expected)


class TestChained(unittest.TestCase):
    def test_attribute(self):
        tree = {'.': {'aaa': {'.': {'bbb': {'.': {'ccc': None}}}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa.bbb.ccc

        self.assertEqual(flytrap.route,
                         [('.', 'aaa'), ('.', 'bbb'), ('.', 'ccc')])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [(),
                          {}])

        temp = lambda a: a.aaa.bbb.ddd
        self.assertRaises(AttributeError, temp, tele)

    def test_call(self):
        tree = {'.': {'aaa': {'.': {'bbb': {'.': {'ccc': {'()': None}}}}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa.bbb.ccc()

        self.assertEqual(flytrap.route,
                         [('.', 'aaa'), ('.', 'bbb'), ('.', 'ccc'), ('()',)])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [(),
                          {}])

        _ = tele.aaa.bbb.ccc('hello')

        self.assertEqual(flytrap.route,
                         [('.', 'aaa'), ('.', 'bbb'), ('.', 'ccc'), ('()',)])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [('hello',),
                          {}])

    def test_getitem(self):
        tree = {'.': {'aaa': {'.': {'bbb': {'.': {'ccc': {'[]': None}}}}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa.bbb.ccc['hello']

        self.assertEqual(flytrap.route,
                         [Node(type='.',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='.',
                               val='bbb',
                               args=None,
                               kwargs=None),
                          Node(type='[]',
                               val='ccc',
                               args='hello',
                               kwargs=None)])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [('hello',),
                          {}])

    def test_deep_call(self):
        tree = {'.': {'aaa': {'.': {'bbb': {'()': {'.': {'ccc': None}}}}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa.bbb('hello', suffix='world').ccc

        self.assertEqual(flytrap.route,
                         [('.', 'aaa'),
                          ('.', 'bbb'),
                          ('()', ('hello',), {'suffix': 'world'}),
                          ('.', 'ccc')])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [(),
                          {}])

    def test_deep_getitem(self):
        tree = {'.': {'aaa': {'.': {'bbb': {'[]': {'.': {'ccc': None}}}}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        _ = tele.aaa.bbb[765].ccc

        self.assertEqual(flytrap.route,
                         [('.', 'aaa'), ('.', 'bbb'), ('[]', 765), ('.', 'ccc')])
        self.assertEqual([flytrap.args,
                          flytrap.kwargs],
                         [(),
                          {}])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(telescope))
    return tests

if __name__ == '__main__':
    unittest.main()





"""
tree = {'()': None,
        '[]': {42: {'()':None}},
        '.':  {'bbb1':None,
               'bbb2':{'()':None}}}

tree = {'()':None,
        '[]':{42:{'()':None},
              9:{'()':None}},
        '.':{'abc':{'()':None},
             'ijk':None}}



#pprint(tree,width=20)

class Flytrap(object):
    def __init__(self):
        self.args = None
        self.kwargs = None

    def f(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class TestBasic(unittest.TestCase):
    def test_basic(self):
        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)

        tele()
        self.assertEqual(flytrap.args, ([('()',)],))

        tele[42]()
        self.assertEqual(flytrap.args, [('[]', 42), ('()',)])

        tele[9]()
        self.assertEqual(flytrap.args, [('[]', 9), ('()',)])

        tele.abc()
        self.assertEqual(flytrap.args, [('.', 'abc'), ('()',)])

        tele.ijk
        self.assertEqual(flytrap.args, [('.', 'ijk')])


        #self.assertEqual(flytrap.val,['aaa1','bbb1'])

'''
spine_properties = {'visible': {'()': None},
                    'bounds': {'()': None},
                    'ticks': {'.': {'major': {'()': None},
                                    'minor': {'()': None}}}}
tree = {'.':{'plot':'()',
             'scatter':'()',
             'xlim':'()',
             'ylim':'()',
             'line':{'label':'()'},
             'spine':{'.':{'left':{'.':spine_properties},
                           'right':{'.':spine_properties},
                           'top':{'.':spine_properties},
                           'bottom':{'.':spine_properties}}}}}
'''

class TestFileLoad(unittest.TestCase):
    def test_file_load(self):
        flytrap = Flytrap()

        path = '/Users/coreygirard/Documents/GitHub/telescope/chart.yml'
        tele = telescope.Telescope(path, print, k='chart')
        tele.spine.left.visible('aaa', 'bbb')
        tele.plot()
        tele.line.label()
        tele.spine.left.visible()
        #self.assertEqual(flytrap.val,[('()',)])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(telescope))
    return tests

if __name__ == '__main__':
    unittest.main()
"""
