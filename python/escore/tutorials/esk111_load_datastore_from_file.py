"""Project: Eskapade - A python-based package for data analysis.

Macro: esk111_load_datastore_from_file

Created: 2018-12-07

Description:
    Macro illustrates how to load an external datastore from file

Authors:
    KMPG AA&BD team

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import shutil
from escore import process_manager, Chain, ConfigObject, DataStore, core_ops
from escore.logger import Logger, LogLevel
from escore.core import persistence

logger = Logger()

logger.debug('Now parsing configuration file esk111_load_datastore_from_file.')

# --- minimal analysis information

settings = process_manager.service(ConfigObject)
settings['analysisName'] = 'esk111_load_datastore_from_file'
settings['version'] = 0

ds = process_manager.service(DataStore)
ds['number'] = 1
file_path = persistence.io_path('proc_service_data','temp_datastore.pkl')
ds.persist_in_file( file_path )

# --- update the number
ds['number'] = 2

# --- Reload from the pickle file with:
# >>> ds = DataStore.import_from_file(file_path)


# --- now set up the chains and links

ch = Chain('Start')
link = core_ops.ImportDataStore(name='importds', path=file_path)
link.logger.log_level = LogLevel.DEBUG
ch.add(link)

link = core_ops.PrintDs()
link.keys = ['number']
ch.add(link)

logger.debug('Done parsing configuration file esk111_load_datastore_from_file.')
