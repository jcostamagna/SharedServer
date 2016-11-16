import unittest

import requests
import json
from test.categoriaTest import TestCategoria
from test.skillTest import TestSkill

if __name__ == '__main__':
    testmodules = [
        'test.categoriaTest',
        'test.skillTest',
        'test.jobPositionsTest'
    ]

    suite = unittest.TestSuite()

    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)
# ~ suite = unittest.TestLoader().loadTestsFromTestCase(TestCategoria)
# ~ unittest.TextTestRunner(verbosity=2).run(suite)
# ~ suite = unittest.TestLoader().loadTestsFromTestCase(TestSkill)
# ~ unittest.TextTestRunner(verbosity=2).run(suite)
