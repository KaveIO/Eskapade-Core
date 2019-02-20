"""Project: Eskapade - A python-based package for data analysis.

Class: SkipChainIfPresent

Created: 2016/11/08

Description:
    Algorithm to skip to the Chain if requested dataset is already present

Authors:
    ING Wholesale Banking Advanced Analytics group

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, DataStore, Link, StatusCode


class SkipChainIfPresent(Link):
    """Sends a SkipChain enums.StatusCode signal when a requested dataset is present.

    This signal causes that the Processs Manager to step immediately to the next Chain.
    """

    def __init__(self, **kwargs):
        """Initialize link instance.

        :param str name: name of link
        :param list collection_set: datastore keys holding the datasets to be checked. If all of these are present,
                                    the chain is skipped.
        :param bool check_at_initialize: if false, perform dataset present check at execute. Default is true.
        :param bool assert_len: assert that each collection has a length greatet than zero. Default is true.
        :param tuple assert_type: types to assert for each object. Default is ().
        """
        Link.__init__(self, kwargs.pop('name', 'SkipChainIfPresent'))

        # process keyword arguments
        self._process_kwargs(kwargs, collection_set=[], check_at_initialize=True, assert_len=True, assert_type=())
        self.check_extra_kwargs(kwargs)

    def initialize(self):
        """Initialize the link."""
        if self.check_at_initialize:
            return self.check_collection_set()

        return StatusCode.Success

    def execute(self):
        """Execute the link.

        Skip to the next Chain if all of the input collections are present.
        """
        if not self.check_at_initialize:
            return self.check_collection_set()

        return StatusCode.Success

    def check_collection_set(self):
        """Check existence of collections in the datastore, and check that they are all present.

        Collections need to be both present and not empty.

        - For pandas dataframes the additional option 'skip_chain_when_key_not_in_ds' exists. Meaning,
          skip the chain as well if the dataframe is not present in the datastore.
        """
        # check if collection names are present in datastore
        ds = process_manager.service(DataStore)

        present = []
        for k in self.collection_set:
            try:
                ds.get(k, assert_len=self.assert_len, assert_type=self.assert_type, assert_in=True)
                present.append(True)
            except:
                present.append(False)

        if len(present)>0 and all(present):
            return StatusCode.SkipChain

        return StatusCode.Success
