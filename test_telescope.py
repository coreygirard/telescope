from pprint import pprint
import unittest
import doctest
import telescope


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
        self.val = None

    def f(self,e):
        self.val = e

class TestBasic(unittest.TestCase):
    def test_basic(self):
        flytrap = Flytrap()
        tele = telescope.Telescope(tree,flytrap.f)
        tele()
        self.assertEqual(flytrap.val,[('()',)])

        tele[42]()
        self.assertEqual(flytrap.val,[('[]',42), ('()',)])

        tele[9]()
        self.assertEqual(flytrap.val,[('[]',9), ('()',)])

        tele.abc()
        self.assertEqual(flytrap.val,[('.','abc'), ('()',)])

        tele.ijk
        self.assertEqual(flytrap.val,[('.','ijk')])


        #self.assertEqual(flytrap.val,['aaa1','bbb1'])


spine_properties = {'visible':{'()':None},
                    'bounds':{'()':None},
                    'ticks':{'.':{'major':{'()':None},
                                  'minor':{'()':None}}}}
tree = {'.':{'plot':'()',
             'scatter':'()',
             'xlim':'()',
             'ylim':'()',
             'line':{'label':'()'},
             'spine':{'.':{'left':{'.':spine_properties},
                           'right':{'.':spine_properties},
                           'top':{'.':spine_properties},
                           'bottom':{'.':spine_properties}}}}}

class TestBasic(unittest.TestCase):
    def test_basic(self):
        flytrap = Flytrap()
        tele = telescope.Telescope('/Users/coreygirard/Documents/GitHub/telescope/chart.yml',print,k='chart')
        tele.spine.left.visible('aaa','bbb')
        tele.plot()
        tele.line.label()
        tele.spine.left.visible()
        #self.assertEqual(flytrap.val,[('()',)])





def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(telescope))
    return tests

if __name__ == '__main__':
    unittest.main()
