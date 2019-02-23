"""Project: Eskapade - A python-based package for data analysis.

Macro: esk112_parallel_fork_demo

Created: 2018-12-26

Description:
    Macro does ...(fill in short description here)

Authors:
    Your name(s) here

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore import process_manager, Chain, ConfigObject, core_ops
from escore.logger import Logger, LogLevel



logger = Logger()
logger.debug('Now parsing configuration file esk112_parallel_fork_demo.')

# --- minimal analysis information

settings = process_manager.service(ConfigObject)
settings['analysisName'] = 'esk112_parallel_fork_demo'
settings['version'] = 0

# --- now set up the chains and links

ch = Chain('Start')
ch.n_fork = 100
fe = core_ops.ForkExample()
fe.store_key = 'forkstoredemo'
fe.logger.log_level = LogLevel.DEBUG
ch.add(fe)

dc = core_ops.ForkDataCollector()
dc.keys = [{'key_ds': fe.store_key, 'func': len}]
dc.logger.log_level = LogLevel.DEBUG
ch.add(dc)

ch = Chain('Overview')
link = core_ops.PrintDs()
link.keys = [fe.store_key]
ch.add(link)

logger.debug('Done parsing configuration file esk112_parallel_fork_demo.')


if __name__ == "__main__":
    import escore
    escore.eskapade_run()
