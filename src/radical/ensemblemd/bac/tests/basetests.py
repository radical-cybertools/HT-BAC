import unittest

from radical.ensemblemd import bac

#-----------------------------------------------------------------------------
#
class Test_Basetests(unittest.TestCase):
    # silence deprecation warnings under py3

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def failUnless(self, expr):
        # St00pid speling.
        return self.assertTrue(expr)

    def failIf(self, expr):
        # St00pid speling.
        return self.assertFalse(expr)

    #-------------------------------------------------------------------------
    #
    def test__check_version(self):
        assert(bac.version != None)