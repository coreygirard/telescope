from pprint import pprint
import unittest
import doctest
import telescope


tree = {'()': None,
        '[]': {42: {'()':None}},
        '.':  {'bbb1':None,
               'bbb2':None}


pprint(tree,width=20)

class Flytrap(object):
    def __init__(self):
        self.val = None

    def f(self,e):
        self.val = e

class Test(unittest.TestCase):
    def test_(self):
        flytrap = Flytrap()
        tele = telescope.Telescope(tree,flytrap.f)

        tele.aaa1.bbb1()

        self.assertEqual(flytrap.val,['aaa1','bbb1'])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(telescope))
    return tests

if __name__ == '__main__':
    unittest.main()
