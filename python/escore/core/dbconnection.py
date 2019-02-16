"""Project: Eskapade - A python-based package for data analysis.

Created: 2017/03/31

Description:
    Eskapade DBConnection class
    The base class for handling database connections with Eskapade's ProcessService

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

from escore.core.mixin import ConfigMixin
from escore.core.process_services import ProcessService

class DbConnection(ProcessService, ConfigMixin):
    """Base class for database connections"""

    _persist = False

    def __init__(self, config_path='', config_section=''):
        """Initialize database connection instance"""

        self._conn = None
        self._config_section = str(config_section) if config_section else ''
        ConfigMixin.__init__(self, config_path=config_path)

    @property
    def connection(self):
        """Underlying database connection"""

        if not self._conn:
            self.create_connection()
        return self._conn

    def create_connection(self):
        """Create the underlying database connection"""
        pass

    @property
    def config_section(self):
        """Section in configuration settings"""

        return self._config_section

    @config_section.setter
    def config_section(self, sec):
        """Set section in configuration settings"""

        sec = str(sec) if sec else ''
        if not sec:
            self.logger.fatal('No configuration section specified for {type}.', type=type(self).__name__)
            raise ValueError('No value specified for configuration section.')
        self._config_section = sec

    def close(self):
        """Close database connection"""
        pass

    def finish(self):
        """Finish database operations"""

        if self._conn:
            self.close()
        self._conn = None
