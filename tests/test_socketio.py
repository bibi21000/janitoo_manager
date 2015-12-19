# -*- coding: utf-8 -*-

"""Unittests for flask.
"""
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
__copyright__ = "Copyright © 2013-2014-2015 Sébastien GALLET aka bibi21000"

import sys, os
import time, datetime
import unittest
import logging

from alembic import command as alcommand
from sqlalchemy import create_engine

from janitoo_manager.app import create_app
from janitoo_manager.extensions import db, plugin_manager, socketio
from janitoo_manager.configs.testing import TestingConfig

from janitoo_nosetests.socketio import JNTTSocketIO, JNTTSocketIOCommon

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

class TestFlask(JNTTSocketIO, JNTTSocketIOCommon):
    """Test SocketIO
    """
    flask_conf = "tests/data/janitoo_manager.conf"

    def setUp(self):
        JNTTSocketIO.setUp(self)
        # Use the testing configuration
        self.config = TestingConfig(self.flask_conf)
        alcommand.upgrade(janitoo_config(self.config.SQLALCHEMY_DATABASE_URI), 'heads')

    def create_app(self):
        # Use the development configuration if available
        config = TestingConfig(self.flask_conf)
        app = create_app(config)
        app.config['LIVESERVER_PORT'] = 8943
        return app, socketio

    def test_001_server_connect(self):
        self.assertConnect("/janitoo")

