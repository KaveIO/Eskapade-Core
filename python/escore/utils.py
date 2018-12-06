"""Project: Eskapade - A python-based package for data analysis.

Created: 2016/11/08

Description:
    Utility functions to collect Eskapade python modules
    e.g. functions to get correct Eskapade file paths and env variables

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import os
import sys

from escore.logger import Logger

ENV_VARS = dict(spark_args='PYSPARK_SUBMIT_ARGS',
                docker='DE_DOCKER', display='DISPLAY')
ARCHIVE_FILE = 'es_python_modules.egg'

logger = Logger()


def set_matplotlib_backend(backend=None, batch=None, silent=True):
    """Set Matplotlib backend.

    :param str backend: backend to set
    :param bool batch: require backend to be non-interactive
    :param bool silent: do not raise exception if backend cannot be set
    :raises: RuntimeError
    """
    try:
        # HACK it's very useful to call this function in the configuration of eskapade,
        # but it's located in eskapade visualization library.
        # this way escore is independent of matplotlib
        # when eskapade is installed, escore is also installed, so this will work.
        # I'm not too happy with this, but will do for now. Think of something better if possible.
        from eskapade.visualization import config
        config.set_matplotlib_backend(backend, batch, silent)
    except (ModuleNotFoundError, AttributeError):
        # eskapade library not found, so nothing to configure
        pass


def get_env_var(key):
    """Retrieve Eskapade-specific environment variables.

    :param str key: Eskapade-specific key to variable
    :returns: environment variable value
    :rtype: str
    """
    var_name = ENV_VARS[key]
    return os.environ.get(var_name)


def check_interactive_backend():
    """Check whether an interactive backend is required
    """
    display = get_env_var('display')

    run_ipynb = in_ipynb()
    run_display = display is None or not display.startswith(':') or not display[1].isdigit()
    if run_ipynb or not run_display:
        # interactive backend required
        return True
    else:
        # non-interactive backend required
        return False


def in_ipynb():
    """Detect whether an Jupyter/Ipython-kernel is being run

    :raises: NameError
    """
    try:
        import IPython.core.getipython as gip
        cfg = gip.get_ipython().config
        if 'IPKernelApp' in cfg.keys():
            #logger.info('Ipython-kernel was found, batch-mode (non-interactive) will be set to false.')
            return True
        else:
            return False
    except (ModuleNotFoundError, AttributeError):
        return False


def in_tty():
    """Detect whether running in a terminal
    """
    import sys
    return sys.stdout.isatty()


def collect_python_modules():
    """Collect Eskapade Python modules."""
    import pathlib
    from pkg_resources import resource_filename
    from zipfile import PyZipFile

    import escore

    package_dir = resource_filename(escore.__name__, '')
    lib_path = pathlib.Path(package_dir).joinpath('lib')
    lib_path.mkdir(exist_ok=True)
    archive_path = str(lib_path.joinpath(ARCHIVE_FILE))

    archive_file = PyZipFile(archive_path, 'w')
    logger.info('Adding Python modules to egg archive {path}.'.format(path=archive_path))
    archive_file.writepy(package_dir)
    archive_file.close()
    return archive_path
