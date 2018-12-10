"""Project: Eskapade - A python-based package for data analysis.

Created: 2017-09-20

Description:
    Helper functions for eskapade_bootstrap

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import datetime
import os
import sys

from escore.logger import Logger

logger = Logger(__name__)


def get_absolute_path(path):
    """Get an absolute path.

    First expands ~ if present. Second take care of any . or ..

    :param path: path
    :returns: the absolute path
    """
    return os.path.abspath(os.path.expanduser(path))


def create_file(path, file_name, content=''):
    """Create a file in a given directory.

    Exit with a status code other than 0 if there is an error.

    :param path: an absolute path to the directory
    :param file_name: file name
    :param content: file's content
    :returns: path to created file
    """
    try:
        logger.info('Creating {file_name} in the directory {dir!s}.', file_name=file_name, dir=path)
        fp = open(path + '/' + file_name, 'w')
    except PermissionError as exc:
        logger.error('Failed to create {file_name} in the directory {dir!s}! error={err!s}.',
                     file_name=file_name, dir=path, err=exc.strerror)
        sys.exit(exc.errno)
    else:
        with fp:
            fp.write(content)


def create_dir(path, is_create_init=False, init_content=''):
    """Create a leaf directory and all intermediate ones.

    Exit with a status code other than 0 if there is an error.

    :param path: an absolute path to the directory
    """
    try:
        logger.info('Creating the directory {dir!s}.', dir=path)
        os.makedirs(path, exist_ok=True)
    except PermissionError as exc:
        logger.error('Failed to create the directory {dir!s}! error={err!s}.', dir=path, err=exc.strerror)
        sys.exit(exc.errno)

    if is_create_init:
        if not init_content:
            init_content = '# Created by Eskapade on {date!s}\n'.format(date=datetime.date.today())
        create_file(path=path,
                    file_name='__init__.py',
                    content=init_content)


def generate_link(link_dir, link_name, is_create_init=False):
    """Generate Eskapade link.

    :param link_dir: absolute path to a directory where the link will be generated
    :param link_name: name of the link to generate
    :param is_create_init: whether to create __init__.py file or no
    """
    # Do not modify the indentation of template!
    template = """\"\"\"Project: Eskapade - A python-based package for data analysis.

Class: {link_name!s}

Created: {date_generated!s}

Description:
    Algorithm to ...(fill in one-liner here)

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
\"\"\"

from escore import process_manager, ConfigObject, DataStore, Link, StatusCode


class {link_name!s}(Link):

    \"\"\"Defines the content of link.\"\"\"

    def __init__(self, **kwargs):
        \"\"\"Initialize an instance.

        :param str name: name of link
        :param str read_key: key of input data to read from data store
        :param str store_key: key of output data to store in data store
        \"\"\"
        # initialize Link, pass name from kwargs
        Link.__init__(self, kwargs.pop('name', '{link_name!s}'))

        # Process and register keyword arguments. If the arguments are not given, all arguments are popped from
        # kwargs and added as attributes of the link. Otherwise, only the provided arguments are processed.
        self._process_kwargs(kwargs, read_key=None, store_key=None)

        # check residual kwargs; exit if any present
        self.check_extra_kwargs(kwargs)
        # Turn off the line above, and on the line below if you wish to keep these extra kwargs.
        # self._process_kwargs(kwargs)

    def initialize(self):
        \"\"\"Initialize the link.

        :returns: status code of initialization
        :rtype: StatusCode
        \"\"\"
        return StatusCode.Success

    def execute(self):
        \"\"\"Execute the link.

        :returns: status code of execution
        :rtype: StatusCode
        \"\"\"
        settings = process_manager.service(ConfigObject)
        ds = process_manager.service(DataStore)

        # --- your algorithm code goes here
        self.logger.debug('Now executing link: {{link}}.', link=self.name)

        return StatusCode.Success

    def finalize(self):
        \"\"\"Finalize the link.

        :returns: status code of finalization
        :rtype: StatusCode
        \"\"\"
        # --- any code to finalize the link follows here

        return StatusCode.Success
"""
    file_name = link_name.lower()

    import_line = 'from .{file_name} import {link_name}'.format(file_name=file_name, link_name=link_name)
    all_line = "__all__ = ['{link_name}', ]".format(link_name=link_name)
    create_file(path=link_dir,
                file_name='{file_name!s}.py'.format(file_name=file_name),
                content=template.format(link_name=link_name, date_generated=datetime.date.today()))
    if is_create_init:
        init_content = '# Created by Eskapade on {date!s}\n{import_line}\n\n{all_line}\n'.format(date=datetime.date.today(),
                                                                                                 import_line=import_line,
                                                                                                 all_line=all_line)
        create_file(path=link_dir,
                    file_name='__init__.py',
                    content=init_content)
    else:
        logger.info('Edit {link_dir}/__init__.py: add \"{link_name}\" to __all__ and add the line "{import_line}".'
                    .format(link_dir=link_dir, file_name=file_name, link_name=link_name, import_line=import_line))


def generate_tests(test_dir: str, package_name: str) -> None:
    """Generate a default test file for new package

    :param test_dir: absolute path to a tests directory
    :param package_name: name of the package
    """
    python_dir = test_dir + '/' + package_name.lower() + '_python'
    create_dir(path=python_dir, is_create_init=True)
    integration_dir = test_dir + '/' + package_name.lower() + '_python/integration'
    create_dir(path=integration_dir, is_create_init=True)

    # 1. setup file
    # Do not modify the indentation of template!
    from setuptools import setup
    template = """# Setup file for tests of {package_name} package.

NAME = '{package_name}_python'

def setup_package() -> None:
    \"\"\"
    The main setup method. It is responsible for setting up and installing the package.
    \"\"\"
    setup(name=NAME,
          license='',
          description='{package_name} test package',
          python_requires='>=3.6',
          packages=['{package_name}_python'],
          install_requires=[]
    )

if __name__ == '__main__':
    setup_package()
"""
    content = template.format(package_name=package_name.lower())
    create_file(path=test_dir, file_name='setup.py', content=content)

    # 2. unit tests file
    # Do not modify the indentation of template!
    template = """# File with unit tests of {package_name} package.

def test_import_{package_name}():
    import {package_name}
"""
    content = template.format(package_name=package_name.lower())
    file_name = package_name.lower()
    create_file(path=python_dir,
                file_name='test_{file_name!s}.py'.format(file_name=file_name), content=content)

    # 3. integration tests file
    # Do not modify the indentation of template!
    template = """# File with integration tests of {package_name} package.

import os
import unittest
import unittest.mock as mock

from escore import process_manager, resources, ConfigObject, DataStore, StatusCode
from escore.bases import TutorialMacrosTest

from {package_name} import resources

class MacrosTest(TutorialMacrosTest):
    \"\"\"Integration tests class for {package_name}\"\"\"

    def test_macro(self):
        self.eskapade_run(resources.macro('macro.py'))

        ds = process_manager.service(DataStore)
        self.assertEqual(0, len(ds.keys()))
"""
    content = template.format(package_name=package_name.lower())
    create_file(path=integration_dir,
                file_name='test_macros.py', content=content)


def generate_macro(macro_dir,
                   macro_name,
                   link_module='core_ops',
                   link_name='HelloWorld',
                   is_create_init=False,
                   import_line='\n'):
    """Generate Eskapade macro.

    :param macro_dir: absolute path to a directory where the macro will be generated
    :param macro_name: name of the macro to generate
    :param link_module: module of a link to import
    :param link_name: name of the link to import
    :param is_create_init: whether to create __init__.py file or no
    """
    # Do not modify the indentation of template!
    template = """\"\"\"Project: Eskapade - A python-based package for data analysis.

Macro: {macro_name!s}

Created: {date_generated!s}

Description:
    Macro does ...(fill in short description here)

Authors:
    Your name(s) here

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
\"\"\"

from escore import process_manager, Chain, ConfigObject, core_ops
from escore.logger import Logger, LogLevel
{import_line!s}

logger = Logger()
logger.debug('Now parsing configuration file {macro_name!s}.')

# --- minimal analysis information

settings = process_manager.service(ConfigObject)
settings['analysisName'] = '{macro_name!s}'
settings['version'] = 0

# --- now set up the chains and links

ch = Chain('Start')
link = {link_module!s}.{link_name!s}()
link.logger.log_level = LogLevel.DEBUG
ch.add(link)

logger.debug('Done parsing configuration file {macro_name!s}.')
"""

    content = template.format(macro_name=macro_name,
                              date_generated=datetime.date.today(),
                              link_module=link_module,
                              link_name=link_name,
                              import_line=import_line)
    if is_create_init:
        init_content = '# Created by Eskapade on {date!s}\n'.format(date=datetime.date.today())
        create_file(path=macro_dir,
                    file_name='__init__.py',
                    content=init_content)
    create_file(path=macro_dir,
                file_name='{macro_name!s}.py'.format(macro_name=macro_name),
                content=content)


def generate_notebook(notebook_dir, notebook_name, macro_path=None):
    """Generate Eskapade notebook.

    :param notebook_dir: absolute path to a directory where the notebook will be generated
    :param notebook_name: name of the notebook to generate
    :param macro_path: absolute path to a macro the notebook executes
    """
    import platform

    from escore import resources

    if macro_path:
        macro_path = "'{path}'".format(path=macro_path)
    else:
        macro_path = "resources.tutorial('esk103_printdatastore.py')"

    with open(resources.template('notebook_template.ipynb')) as file:
        template = file.read()
        content = template.format(macro_path=macro_path,
                                  notebook_name=notebook_name,
                                  python_version=platform.python_version())
        create_file(path=notebook_dir,
                    file_name='{notebook_name!s}.ipynb'.format(notebook_name=notebook_name),
                    content=content)


def generate_configs(root_dir: str) -> None:
    """Generate default configs.

    :param str root_dir: Absolute path to package root directory.
    """
    config_dir = root_dir + '/config/'
    create_dir(config_dir)


def generate_python_dir(root_dir: str, package_name: str) -> None:
    """Generate default configs.

    :param str root_dir: Absolute path to package root directory.
    :param str package_name: Name of the package.
    """
    python_dir   = root_dir + '/' + package_name
    init_str = "# flake8: noqa\nfrom {0:s}.version import version as __version__\n".format(package_name)
    create_dir(python_dir, is_create_init=True, init_content=init_str)


def generate_resources(python_dir: str, package_name: str) -> None:
    """Generate project resources.py.

    :param python_dir: absolute path to an analysis project python dir
    :param package_name: package name
    """
    # Do not modify the indentation of template!
    template = """# Resources lookup file for {package_name}
# Created by Eskapade on {date}

import pathlib
import sys

from pkg_resources import resource_filename

import {package_name}

# macros that are shipped with {package_name}.
_MACROS = dict((_.name, _) for _ in pathlib.Path(resource_filename({package_name}.__name__, 'macros')).glob('*.py'))

# notebooks that are shipped with {package_name}.
_NOTEBOOKS = dict((_.name, _) for _ in pathlib.Path(resource_filename({package_name}.__name__, 'notebooks')).glob('*.ipynb'))

# configuration files that are shipped with {package_name}.
_CONFIGS = dict((_.name, _) for _ in pathlib.Path(resource_filename({package_name}.__name__, 'config')).glob('*'))

# data files that are shipped with {package_name}.
_DATA = dict((_.name, _) for _ in pathlib.Path(resource_filename({package_name}.__name__, 'data')).glob('*'))

# Resource types
_RESOURCES = dict(macro=_MACROS, config=_CONFIGS, notebook=_NOTEBOOKS, data=_DATA)


def _resource(resource_type, name: str) -> str:
    \"\"\"Return the full path filename of a resource.

    :param str resource_type: The type of the resource.
    :param str  name: The name of the resource.
    :returns: The full path filename of the fixture data set.
    :rtype: str
    :raises FileNotFoundError: If the resource cannot be found.
    \"\"\"
    full_path = _RESOURCES[resource_type].get(name, None)

    if full_path and full_path.exists():
        return str(full_path)

    raise FileNotFoundError('Could not find {resource_type_str} {name_str}! Does it exist?'
                            .format(resource_type=resource_type, name=name))


def macro(name: str) -> str:
    \"\"\"Return the full path filename of a shipped macro.

    :param str name: The name of the macro.
    :returns: The full path filename of the macro.
    :rtype: str
    :raises FileNotFoundError: If the macro cannot be found.
    \"\"\"
    return _resource('macro', name)


def notebook(name: str) -> str:
    \"\"\"Return the full path filename of a shipped notebook.

    :param str name: The name of the notebook.
    :returns: The full path filename of the notebook.
    :rtype: str
    :raises FileNotFoundError: If the notebook cannot be found.
    \"\"\"
    return _resource('notebook', name)


def data(name: str) -> str:
    \"\"\"Return the full path filename of a shipped data file.

    :param str name: The name of the data.
    :returns: The full path filename of the data.
    :rtype: str
    :raises FileNotFoundError: If the data cannot be found.
    \"\"\"
    return _resource('data', name)


def config(name: str) -> str:
    \"\"\"Return the full path filename of a shipped config file.

    :param str name: The name of the config.
    :returns: The full path filename of the config.
    :rtype: str
    :raises FileNotFoundError: If the config cannot be found.
    \"\"\"
    return _resource('config', name)
"""
    resource_type_str = '{resource_type}'
    name_str = '"{name!s}"'
    content = template.format(package_name=package_name.lower(), resource_type_str=resource_type_str,
                              name_str=name_str, date=datetime.date.today())
    create_file(path=python_dir, file_name='resources.py', content=content)


def generate_entry_points(python_dir: str, package_name: str) -> None:
    """Generate project's entry_points.py.

    :param python_dir: absolute path to an analysis project python dir
    :param package_name: package name
    """
    # Do not modify the indentation of template!
    template = """# Entry points for {package_name}
# See setup.py for defined entry_point scripts
# Created by Eskapade on {date}

from escore.logger import LogLevel, Logger, global_log_publisher, ConsoleHandler, ConsoleErrHandler

publisher = global_log_publisher
publisher.log_level = LogLevel.INFO
publisher.add_handler(ConsoleHandler())
publisher.add_handler(ConsoleErrHandler())

logger = Logger(__name__)


def trial():
    \"\"\"Run {package_name} tests.

    This function is just a wrapper around pytest.
    Will keep this here until fully switched to pytest or nose and tox.
    \"\"\"
    import sys
    import pytest

    # ['--pylint'] +
    # -r xs shows extra info on skips and xfails.
    default_options = ['-rxs']
    args = sys.argv[1:] + default_options
    sys.exit(pytest.main(args))


def run():
    \"\"\"Run {package_name} program.
    \"\"\"
    import argparse
    parser = argparse.ArgumentParser('{package_name}_run',
                                     description='Run entry point for {package_name}.')
    args = parser.parse_args()

    logger.info('Welcome to {package_name}!')
"""
    content = template.format(package_name=package_name.lower(), date=datetime.date.today())
    create_file(path=python_dir, file_name='entry_points.py', content=content)


def generate_readme(root_dir: str, package_name: str) -> None:
    """Generate empty project readme.

    :param root_dir: absolute path to an analysis project root dir
    :param package_name: package name
    """
    # create empty readme
    line = '=' * len(package_name)
    readme_str = '{0}\n{1}\n{0}\n\n* Version: {2}\n* Released: {3}\n'.format(line, package_name, '1.0.0.dev', datetime.date.today())
    create_file(path=root_dir, file_name='README.rst', content=readme_str)


def generate_setup(root_dir: str, package_name: str) -> None:
    """Generate project setup.py.

    :param root_dir: absolute path to an analysis project root dir
    :param package_name: package name
    """
    # Do not modify the indentation of template!
    template = """from setuptools import setup, find_packages

NAME = '{package_name}'

MAJOR = 1
REVISION = 0
PATCH = 0
DEV = True

VERSION = '{{major}}.{{revision}}.{{patch}}'.format(major=MAJOR, revision=REVISION, patch=PATCH)
FULL_VERSION = VERSION
if DEV:
    FULL_VERSION += '.dev'

TEST_REQUIREMENTS = ['pytest>=3.5.0',
                     'pytest-pylint>=0.9.0',
                     ]
REQUIREMENTS = [
    'Eskapade-Core>=0.9.3'
    ]

REQUIREMENTS = REQUIREMENTS + TEST_REQUIREMENTS

def write_version_py(filename: str = '{package_name}/version.py') -> None:
    \"\"\"Write package version to version.py.

    This will ensure that the version in version.py is in sync with us.

    :param filename: The version.py to write too.
    :type filename: str
    \"\"\"
    # Do not modify the indentation of version_str!
    version_str = \"\"\"\\\"\\\"\\\"THIS FILE IS AUTO-GENERATED BY SETUP.PY.\\\"\\\"\\\"

{name_str}
{version_str}
{full_version_str}
{release_str}
\"\"\"

    version_file = open(filename, 'w')
    try:
        version_file.write(version_str.format(name=NAME.lower(),
                                              version=VERSION,
                                              full_version=FULL_VERSION,
                                              is_release=not DEV))
    finally:
        version_file.close()


def setup_package() -> None:
    \"\"\"The main setup method.

    It is responsible for setting up and installing the package.
    \"\"\"
    write_version_py()

    setup(name=NAME,
          version=VERSION,
          python_requires='>=3.6',
          packages=find_packages(),
          install_requires=REQUIREMENTS,
          tests_require=TEST_REQUIREMENTS,
          # files to be shipped with the installation, under: {package_name}/{package_name}/
          # after installation, these can be found with the functions in resources.py
          package_data=dict({package_name}=[\'config/*\', \'notebooks/*.ipynb\', \'data/*\']),
          # The following 'creates' executable scripts for *nix and Windows.
          # The Windows scripts will auto-magically get a .exe extension.
          # {package_name}_run:   example main application of package.
          # {package_name}_trial: test application to let loose on tests. This is just a wrapper around pytest.
          # See: entry_points.py for run() and trail() functions. cmd line args are passed on.
          entry_points=dict(
              console_scripts = [
                  '{package_name}_run = {package_name}.entry_points:run',
                  '{package_name}_trial = {package_name}.entry_points:trial'
              ]
          )
    )


if __name__ == '__main__':
    setup_package()
"""
    name_str = "name = '{name!s}'"
    version_str = "version = '{version!s}'"
    full_version_str = "full_version = '{full_version!s}'"
    release_str = "release = {is_release!s}"
    content = template.format(package_name=package_name.lower(), name_str=name_str, version_str=version_str,
                              full_version_str=full_version_str, release_str=release_str)
    create_file(path=root_dir, file_name='setup.py', content=content)
