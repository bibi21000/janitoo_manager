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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"

import sys, os
import time, datetime
import unittest
import logging

from flask import Flask, session, request

from alembic import command as alcommand
from sqlalchemy import create_engine

from janitoo_manager.app import create_app
from janitoo_manager.extensions import db, socketio
from janitoo_manager.configs.testing import TestingConfig

from janitoo_nosetests_flask.socketio import JNTTSocketIO, JNTTSocketIOCommon
from janitoo_nosetests import JNTTBase

from janitoo.utils import json_dumps, json_loads
from janitoo.utils import HADD_SEP, HADD
from janitoo.utils import TOPIC_HEARTBEAT
from janitoo.utils import TOPIC_NODES, TOPIC_NODES_REPLY, TOPIC_NODES_REQUEST
from janitoo.utils import TOPIC_BROADCAST_REPLY, TOPIC_BROADCAST_REQUEST
from janitoo.utils import TOPIC_VALUES_USER, TOPIC_VALUES_CONFIG, TOPIC_VALUES_SYSTEM, TOPIC_VALUES_BASIC

from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

from . import ManagerCommon

class TestSocketIO(ManagerCommon, JNTTSocketIO, JNTTSocketIOCommon):
    """Test SocketIO
    """
    flask_conf = "tests/data/janitoo_manager.conf"

    def test_101_network_starting(self):
        self.connect()
        received = self.client.get_received(self.namespace)
        #~ print received
        time.sleep(5)
        received = self.client.get_received(self.namespace)
        print(received)
        self.assertTrue(len(received) > 1)

    def test_111_event_network(self):
        event = "my network event"
        response = "my network response"
        self.connect()
        received = self.client.get_received(self.namespace)
        #~ print received
        time.sleep(1)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.client.emit(event, {})
        time.sleep(5)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.assertTrue(len(received) >= 1)
        self.assertEqual(len(received[0]['args']), 1)
        data = {}
        for res in received:
            data[res['name']] = res['args'][0]['data']
        print(data)
        self.assertTrue(response in data)
        self.assertEqual(data[response]['state'], 'STARTED')

    def test_121_event_nodes(self):
        self.wipTest()
        response = "my nodes response"
        event = "my nodes event"
        self.connect()
        received = self.client.get_received(self.namespace)
        #~ print received
        time.sleep(90)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.client.emit(event, {})
        time.sleep(10)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.assertTrue(len(received) >= 1)
        self.assertEqual(len(received[0]['args']), 1)
        data = {}
        for res in received:
            data[res['name']] = res['args'][0]['data']
        print(data)
        self.assertTrue(response in data)
        self.assertEqual(data[response]['state'], ('STARTED',))

    def test_131_event_basics(self):
        self.wipTest()
        response = "my basics response"
        event = "my basics event"
        self.connect()
        received = self.client.get_received(self.namespace)
        #~ print received
        time.sleep(90)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.client.emit(event, {})
        time.sleep(10)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.assertTrue(len(received) >= 1)
        self.assertEqual(len(received[0]['args']), 1)
        data = {}
        for res in received:
            data[res['name']] = res['args'][0]['data']
        print(data)
        self.assertTrue(response in data)

    def test_141_event_system(self):
        self.wipTest()
        response = "my systems response"
        event = "my systems event"
        self.connect()
        received = self.client.get_received(self.namespace)
        #~ print received
        time.sleep(90)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.client.emit(event, {})
        time.sleep(10)
        received = self.client.get_received(self.namespace)
        #~ print received
        self.assertTrue(len(received) >= 1)
        self.assertEqual(len(received[0]['args']), 1)
        data = {}
        for res in received:
            data[res['name']] = res['args'][0]['data']
        print(data)
        self.assertTrue(response in data)
