import unittest
import doctest
import telescope


Node = telescope.Node

class Flytrap(object):
    def __init__(self):
        self.route = None

    def f(self, route):
        self.route = route


class TestInit(unittest.TestCase):
    def test_init(self):
        tree = {'aaa': None}

        class Testing(telescope.telehelper(tree)):
            def handle(self, *args, **kwargs):
                print('hello', args, kwargs)

        t = Testing()
        t.aaa

        #temp = lambda a: a.bbb
        #self.assertRaises(AttributeError, temp, t)

'''
class TestCallableRoot(unittest.TestCase):
    def test_callable_root(self):
        tree = {'()': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele()

        expected = [Node(type='()',
                         val=None,
                         args=(),
                         kwargs={})]

        self.assertEqual(flytrap.route,
                         expected)

    def test_callable_root_with_args(self):
        tree = {'()': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele(123, '456')

        expected = [Node(type='()',
                         val=None,
                         args=(123, '456'),
                         kwargs={})]

        self.assertEqual(flytrap.route,
                         expected)

class TestAttribute(unittest.TestCase):
    def test_attribute(self):
        tree = {'aaa': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None)])

        temp = lambda a: a.bbb
        self.assertRaises(AttributeError, temp, tele)

class TestElement(unittest.TestCase):
    def test_element(self):
        tree = {'[]': None}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele['abc']

        self.assertEqual(flytrap.route,
                         [Node(type='[]',
                               val=None,
                               args='abc',
                               kwargs=None)])

class TestFileLoad(unittest.TestCase):
    def test_file_load(self):
        result = telescope.build_tree('chart.yml')
        expected = {'bbb': None,
                    'ccc': {'[]': None},
                    'ddd': {'()': None},
                    'eee': {'jjj': None}}
        self.assertEqual(result, expected)

class TestChained(unittest.TestCase):
    def test_attribute(self):
        tree = {'aaa': {'bbb': {'ccc': None}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb.ccc

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='attr',
                               val='bbb',
                               args=None,
                               kwargs=None),
                          Node(type='attr',
                               val='ccc',
                               args=None,
                               kwargs=None)])

        temp = lambda a: a.aaa.bbb.ddd
        self.assertRaises(AttributeError, temp, tele)

    def test_call(self):
        tree = {'aaa': {'bbb': {'ccc': {'()': None}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb.ccc()

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='attr',
                               val='bbb',
                               args=None,
                               kwargs=None),
                          Node(type='()',
                               val='ccc',
                               args=(),
                               kwargs={})])

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb.ccc('hello')

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='attr',
                               val='bbb',
                               args=None,
                               kwargs=None),
                          Node(type='()',
                               val='ccc',
                               args=('hello',),
                               kwargs={})])

    def test_getitem(self):
        tree = {'aaa': {'bbb': {'ccc': {'[]': None}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb.ccc['hello']

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='attr',
                               val='bbb',
                               args=None,
                               kwargs=None),
                          Node(type='[]',
                               val='ccc',
                               args='hello',
                               kwargs=None)])

    def test_deep_call(self):
        tree = {'aaa': {'bbb': {'()': {'ccc': None}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb('hello', suffix='world').ccc

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='()',
                               val='bbb',
                               args=('hello',),
                               kwargs={'suffix': 'world'}),
                          Node(type='attr',
                               val='ccc',
                               args=None,
                               kwargs=None)])

    def test_deep_getitem(self):
        tree = {'aaa': {'bbb': {'[]': {'ccc': None}}}}

        flytrap = Flytrap()
        tele = telescope.Telescope(tree, flytrap.f)
        tele.aaa.bbb[765].ccc

        self.assertEqual(flytrap.route,
                         [Node(type='attr',
                               val='aaa',
                               args=None,
                               kwargs=None),
                          Node(type='[]',
                               val='bbb',
                               args=765,
                               kwargs=None),
                          Node(type='attr',
                               val='ccc',
                               args=None,
                               kwargs=None)])

'''
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(telescope))
    return tests

if __name__ == '__main__':
    unittest.main()
