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

from alembic import command as alcommand
from sqlalchemy import create_engine
from alembic import command as alcommand

from flask_themes2 import get_themes_list
from flask import url_for

from janitoo_manager.app import create_app
from janitoo_manager.extensions import db, socketio
from janitoo_manager.configs.testing import TestingConfig

from janitoo_nosetests_flask.flask import JNTTFlask, JNTTFlaskCommon
#~ from janitoo_nosetests_flask.flask import JNTTFlaskLive, JNTTFlaskLiveCommon
from janitoo_nosetests import JNTTBase

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo.options import JNTOptions
from janitoo_db.base import Base, create_db_engine
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

class TestApp(ManagerCommon, JNTTBase):
    """Test app
    """
    def test_001_create_app(self):
        app = self.create_app()
        app.extensions['janitoo'].start_listener()
        time.sleep(10)
        app.extensions['janitoo'].stop_listener()
        del app.extensions['janitoo']
        app = None
        #~ self.assertTrue(False)

class TestFlask(ManagerCommon, JNTTFlask, JNTTFlaskCommon):
    """Test flask
    """

    def test_101_admin_endpoints(self):
        print self.get_routes()
        self.assertEndpoint('admin.nodes')
        self.assertEndpoint('admin.values_user')

    def test_151_load_themes(self):
        app = self.app
        themes = get_themes_list()
        themes_names = [ t.name for t in themes ]
        print "themes_names %s" % themes_names
        self.assertTrue('Admin' in themes_names)
        self.assertTrue('Bootstrap3' in themes_names)
        self.assertTrue('Bootstrap2' in themes_names)
        themes_identifiers = [ t.identifier for t in themes ]
        self.assertTrue('admin' in themes_identifiers)
        self.assertTrue('bootstrap3' in themes_identifiers)
        self.assertTrue('bootstrap2' in themes_identifiers)

    def test_201_admin_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/', "200 OK")
        #~ self.assertTrue(False)

    def test_202_bower_bootstrap(self):
        self.list_routes()
        self.assertEqual(url_for('bower.static', filename='bootstrap/dist/css/bootstrap.min.css'), '/bower/bootstrap/dist/css/bootstrap.min.css?version=3.3.6')

    def test_211_values_basic_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/values_basic', "200 OK")

    def test_212_values_system_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/values_system', "200 OK")

    def test_213_values_config_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/values_config', "200 OK")

    def test_214_values_command_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/values_command', "200 OK")

    def test_215_values_user_is_up(self):
        self.list_routes()
        self.assertUrl('/admin/values_user', "200 OK")
