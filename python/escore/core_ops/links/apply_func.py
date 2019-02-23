"""Project: Eskapade - A python-based package for data analysis.

Class: ApplyFunc

Created: 2018-12-29

Description:
    Algorithm that applies a function to an object in the datastore

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, ConfigObject, DataStore, Link, StatusCode
import copy

class ApplyFunc(Link):

    """Algorithm that applies a function to an object in the datastore."""

    def __init__(self, *args, **kwargs):
        """Initialize an instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store
        :param default: The default value of the key in case not found.
        :param assert_type: if set, check object for given type or tuple of types. If fails, raise TypeError.
        :param bool assert_len: if true, check that object has length greater than 0. If fails, raise TypeError or AssertionError.
        :param bool assert_in: assert that key is known, default is true.
        :param func: function to execute
        :param args: all args are passed pass to function as args.
        :param kwargs: all other key word arguments are passed on to the function as kwargs.
        :param str store_key: key of output data to store in data store
        """
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', 'ApplyFunc'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs,
                             read_key = '',
                             default = None,
                             assert_type = None,
                             assert_len = False,
                             assert_in = True,
                             func = None,
                             store_key='')

        # pass on remaining kwargs to pandas reader
        self.args = copy.deepcopy(args)
        self.kwargs = copy.deepcopy(kwargs)

    def initialize(self):
        """Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        """
        if not isinstance(self.read_key, (str, list)):
            raise TypeError('read_key should be a string or list of strings.')
        self.check_arg_types(store_key=str)
        if self.func is None:
            raise AssertionError('Input function not set.')

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        """
        ds = process_manager.service(DataStore)

        if self.read_key:
            # fetch and check input
            if isinstance(self.read_key, str):
                obj = ds.get(self.read_key, self.default, self.assert_type, self.assert_len, self.assert_in)
            elif isinstance(self.read_key, list):
                obj = [ds.get(key, self.default, self.assert_type, self.assert_len, self.assert_in) for key in self.read_key]
            # apply function
            trans_obj = self.func(obj, *self.args, **self.kwargs)
        else:
            # possibly function does not require object as input
            trans_obj = self.func(*self.args, **self.kwargs)

        if self.store_key:
            ds[self.store_key] = trans_obj

        return StatusCode.Success
