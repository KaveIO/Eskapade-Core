"""Project: Eskapade - A python-based package for data analysis.

Class: ForkDataCollector

Created: 2018-12-26

Description:
    Algorithm to collect and merge objects from the datastore during a fork.

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, ConfigObject, DataStore, ForkStore, Link, StatusCode

def unit_func(x):
    return x

class ForkDataCollector(Link):

    """Defines the content of link."""

    def __init__(self, **kwargs):
        """Initialize an instance.

        :param str name: name of link
        :param list keys: functions to apply (list of dicts)
          - 'key_ds' (string): input key in datastore
          - 'key_fs' (string, optional): output key in forkstore
          - 'func': function to apply, optional
          - 'append': if key_ds points to a list, append each item to list in forkstore. Default is True.
          - 'args' (tuple, optional): args for 'func'
          - 'kwargs' (dict, optional): kwargs for 'func'
        """
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', 'ForkDataCollector'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs, keys=[])

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off the line above, and on the line below if you wish to keep these extra kwargs.
        # self._process_kwargs(kwargs)

    def initialize(self):
        """Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        """
        if not self.keys:
            self.logger.warning('No functions to apply')

        # perform basic checks on input keys
        for idx in range(len(self.keys)):
            if isinstance(self.keys[idx], str):
                arr = self.keys[idx]
                arr = dict(key_fs=arr, key_ds=arr, func=unit_func)
                self.keys[idx] = arr
            if not isinstance(self.keys[idx], dict):
                raise AssertionError('keys attribute is not a list of dict/str.')
            arr = self.keys[idx]
            keys = list(arr.keys())
            if 'key_ds' not in keys:
                raise AssertionError('key input is insufficient.')

        # will count number of times execute has been called.
        fs = process_manager.service(ForkStore)
        fs['n_'+self.name+'_executed'] = 0

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        """
        settings = process_manager.service(ConfigObject)
        if not 'fork' in settings:
            # nothing to do
            return StatusCode.Success
        fidx = settings.get('fork_index', 0)

        ds = process_manager.service(DataStore)
        fs = process_manager.service(ForkStore)

        # collecting inputs from datastore and adding to forkstore
        for arr in self.keys:
            keys = list(arr.keys())
            key_ds = arr['key_ds']
            assert key_ds in ds, 'key {} not in datastore'.format(key_ds)
            key_fs = key_ds if 'key_fs' not in keys else arr['key_fs']
            append_items = True if 'append' not in keys else arr['append']
            # make sure forkstore is unlocked, then lock
            #fs.wait_until_unlocked()
            with fs.lock:
                fs['n_'+self.name+'_executed'] += 1
                #EOFError: Ran out of input
                #_pickle.UnpicklingError: invalid load key, '\x00'.
                # make sure of order
                temp_list = fs.get(key_fs, [])
                obj = ds[key_ds]
                if not isinstance(obj, list):
                    temp_list.append(obj)
                else:
                    if append_items:
                        temp_list += obj
                    else:
                        temp_list.append(obj)
                fs[key_fs] = temp_list

        return StatusCode.Success

    def finalize(self):
        """Finalize the link.

        :returns: status code of finalization
        :rtype: StatusCode
        """
        ds = process_manager.service(DataStore)
        fs = process_manager.service(ForkStore)

        # check if nothing to do
        if fs.get('n_'+self.name+'_executed', 0) == 0:
            return StatusCode.Success
        # check number of times forkdatacollector has run
        if fs.get('n_fork', 0) > 0 and (fs['n_'+self.name+'_executed'] % fs['n_fork'] > 0):
            self.logger.warning('Did not execute multiple of n_fork {0} times: {1}. Data may be missing.'.format(fs['n_fork'], fs['n_'+self.name+'_executed']))

        # putting (transformed) objects from forkstore back into datastore
        for arr in self.keys:
            keys = list(arr.keys())
            key_ds = arr['key_ds']
            key_fs = key_ds if 'key_fs' not in keys else arr['key_fs']
            if key_fs not in fs:
                raise AssertionError('key {} not in forkstore.'.format(key_fs))
            # retrieve function to apply
            func = unit_func if 'func' not in keys else arr['func']
            args = () if 'args' not in keys else arr['args']
            kwargs = {} if 'kwargs' not in keys else arr['kwargs']
            # apply transformation
            self.logger.debug('Applying function {function!s}.', function=func)
            obj = fs[key_fs]
            try:
                trans_obj = func(obj, *args, **kwargs)
            except:
                raise Exception('Failed to apply function {function!s} to object with {key}.', function=func, key=key_ds)
            # put transformed ojbect back in datastore
            ds[key_ds] = trans_obj

        fs.Print()

        return StatusCode.Success
