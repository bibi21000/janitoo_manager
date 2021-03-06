# -*- coding: utf-8 -*-
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import sys, os
import time, datetime
import unittest

from alembic import command as alcommand
from sqlalchemy import create_engine
from alembic import command as alcommand

from flask_themes2 import get_themes_list
from flask import url_for

from janitoo_manager.app import create_app
from janitoo_manager.extensions import db, socketio
from janitoo_manager.configs.testing import TestingConfig

from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

class ManagerCommon(object):
    """Test flask
    """
    flask_conf = "tests/data/janitoo_manager.conf"

    def create_app(self):
        # Use the testing configuration
        self.config = TestingConfig(self.flask_conf)
        alcommand.upgrade(janitoo_config(self.config.SQLALCHEMY_DATABASE_URI), 'heads')
        app = create_app(self.config)
        app.config['LIVESERVER_PORT'] = 8943
        return app
