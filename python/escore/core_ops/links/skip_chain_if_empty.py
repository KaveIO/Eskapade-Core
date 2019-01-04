"""Project: Eskapade - A python-based package for data analysis.

Class: SkipChainIfEmpty

Created: 2016/11/08

Description:
    Algorithm to skip to the next Chain if input dataset is empty

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, DataStore, Link, StatusCode


class SkipChainIfEmpty(Link):
    """Sends a SkipChain enums.StatusCode signal when an appointed dataset is empty.

    This signal causes that the Processs Manager to step immediately to the next Chain.
    Input collections can be either mongo collections or dataframes in the datastore.
    """

    def __init__(self, **kwargs):
        """Initialize link instance.

        :param str name: name of link
        :param list collection_set: datastore keys holding the datasets to be checked. If any of these is empty,
                                    the chain is skipped.
        :param bool skip_missing: skip the chain if the dataframe is not present in the
                                  datastore. Default is True.
        :param bool skip_zero_len: skip the chain if the object is found in the datastore but has zero length. Default is True.
        :param bool check_at_initialize: perform dataset empty is check at initialize. Default is true.
        """
        Link.__init__(self, kwargs.pop('name', 'SkipChainIfEmpty'))

        # process keyword arguments
        self._process_kwargs(kwargs, collection_set=[], skip_missing=True, skip_zero_len=True,
                             check_at_initialize=True, check_at_execute=False)
        self.check_extra_kwargs(kwargs)

    def initialize(self):
        """Initialize the link."""
        if self.check_at_initialize:
            return self.check_collection_set()

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        Skip to the next Chain if any of the input dataset is empty.
        """
        if not self.check_at_initialize or self.check_at_execute:
            return self.check_collection_set()

        return StatusCode.Success

    def check_collection_set(self):
        """Check existence of collection in the datastore, and check if they are empty.

        All collections need to be both present and not empty for the chain to be continued.
        """
        ds = process_manager.service(DataStore)

        # check if requested collection names are present in datastore
        # if anyone is missing, skip the chain
        for k in self.collection_set:
            if k not in ds:
                if self.skip_missing: # default is true
                    self.logger.info('Key {key!s} not in DataStore. Skipping chain as requested.', key=k)
                    return StatusCode.SkipChain
                else:
                    self.logger.warning('Key {key!s} not in DataStore. Continuing nonetheless.', key=k)
                    continue
            obj = ds[k]
            if self.skip_zero_len: # default is true
                try:
                    obj_length = len(obj)
                    if obj_length == 0:
                        self.logger.info('object with key {key} has zero length. Skipping chain as requested.', key=k)
                        return StatusCode.SkipChain
                    else:
                        self.logger.debug('object with key {key} has length {n}. Continuing.', key=k, n=obj_length)
                        continue
                except Exception as e: #TypeError:
                    self.logger.error('object with key {key} has no len() function.', key=k)
                    raise e

        return StatusCode.Success
