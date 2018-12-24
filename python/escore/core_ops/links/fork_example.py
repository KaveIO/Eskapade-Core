"""Project: Eskapade - A python-based package for data analysis.

Class: ForkExample

Created: 2018-12-26

Description:
    Algorithm to illustrate to how retrieve information of a forked process

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, ConfigObject, DataStore, ForkStore, Link, StatusCode


class ForkExample(Link):

    """Defines the content of link."""

    def __init__(self, **kwargs):
        """Initialize an instance.

        :param str name: name of link
        :param str store_key: key of object to store in data store
        """
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', 'ForkExample'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs, store_key='forkdatacollector')

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off the line above, and on the line below if you wish to keep these extra kwargs.
        # self._process_kwargs(kwargs)

    def initialize(self):
        """Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        """
        # counter how often this link has been executed.
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
            return StatusCode.Success
        # this is a forked process!

        ds = process_manager.service(DataStore)
        fs = process_manager.service(ForkStore)

        # retrieve the index of the forked process
        fidx = settings.get('fork_index', 0)
        self.logger.debug('Now executing link: {link}. Fork index: {fidx}', link=self.name, fidx=fidx)

        # store a number for later collection
        ds[self.store_key] = fidx

        # count how often this loop has been executed (including loops!).
        # make sure forkstore is unlocked, then lock
        #fs.wait_until_unlocked()
        with fs.lock:
            self.logger.info('Fork {} is locked.'.format(fidx))
            fs['n_'+self.name+'_executed'] += 1
        self.logger.info('Fork {} is unlocked.'.format(fidx))

        # fs['exec_index'] += 1 is not stable for some reason?
        # https://stackoverflow.com/questions/38703907/modify-a-list-in-multiprocessing-pools-manager-dict

        self.logger.debug('Done executing link: {link}. Fork index: {fidx}', link=self.name, fidx=fidx)

        return StatusCode.Success

    def finalize(self):
        """Finalized the link.

        :returns: status code of finalize
        :rtype: StatusCode
        """
        fs = process_manager.service(ForkStore)
        self.logger.info('Link {link} has been executed {loop} times.', link=self.name, loop=fs['n_'+self.name+'_executed'])

        return StatusCode.Success
