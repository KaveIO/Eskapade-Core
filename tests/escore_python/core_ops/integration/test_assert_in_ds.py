import unittest

from escore_python.observers import MockDataStoreObserver, TestCaseObservable


class AssertInDsTest(unittest.TestCase, TestCaseObservable):

    def setUp(self):
        observers = [MockDataStoreObserver()]
        super(AssertInDsTest, self).set_up_observers(observers)

    def test_execute(self):
        from escore import process_manager
        from escore import DataStore
        from escore.core_ops.links import AssertInDs

        ds = process_manager.service(DataStore)
        ds['test1'] = {'test1': 1}
        ds['test2'] = {'test2': 2}
        ds['test3'] = {'test3': 3}
        aids = AssertInDs()

        aids.keySet = ['test1', 'test2', 'test3']

        aids.initialize()
        aids.execute()
        aids.finalize()

        # There is no output to test against.
        self.assertIn('test1', ds, 'dict not in datastore')
        self.assertIn('test2', ds, 'dict not in datastore')
        self.assertIn('test3', ds, 'dict not in datastore')

    def tearDown(self):
        super(AssertInDsTest, self).tear_down_observers()
        from escore.core import execution
        execution.reset_eskapade()
