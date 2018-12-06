import unittest

from escore_python.observers import MockDataStoreObserver, TestCaseObservable


class DsToDsTest(unittest.TestCase, TestCaseObservable):

    def setUp(self):
        observers = [MockDataStoreObserver()]
        super(DsToDsTest, self).set_up_observers(observers)

    def test_execute(self):
        from escore import process_manager, DataStore
        from escore.core_ops.links import DsToDs

        ds = process_manager.service(DataStore)
        ds['test'] = 1
        ds_to_ds = DsToDs()
        ds_to_ds.read_key = 'test'
        ds_to_ds.store_key = 'moved_test'
        ds_to_ds.execute()

        self.assertIn('moved_test', ds, 'new key not in datastore')
        self.assertNotIn('test', ds, 'old key still in datastore')
        self.assertEqual(ds['moved_test'], 1, 'key-value pair not consistent')

    def tearDown(self):
        super(DsToDsTest, self).tear_down_observers()
        from escore.core import execution
        execution.reset_eskapade()
