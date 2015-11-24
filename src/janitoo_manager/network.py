# -*- coding: utf-8 -*-
"""The Node

about the pollinh mechanism :
 - simplest way to do it : define a poll_thread_timer for every value that needed to publish its data
 - Add a kind of polling queue that will launch the method to get and publish the value

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

# Set default logging handler to avoid "No handler found" warnings.
import logging
logger = logging.getLogger( 'janitoo.manager' )
import threading
import datetime
from flask import request
from janitoo.value import JNTValue
from janitoo.node import JNTNode
from janitoo.utils import HADD, HADD_SEP, json_dumps, json_loads, hadd_split
from janitoo.dhcp import HeartbeatMessage, check_heartbeats, CacheManager, JNTNetwork
from janitoo.mqtt import MQTTClient
from janitoo.options import JNTOptions

def extend( self ):

    def emit_nodes():
        """Emit a nodes state event
        """
        res = {}
        res.update(self.nodes)
        for key in res:
            add_ctrl, add_node = hadd_split(key)
            if add_ctrl in self.heartbeat_cache.entries and add_node in self.heartbeat_cache.entries[add_ctrl]:
                res[key]['state'] = self.heartbeat_cache.entries[add_ctrl][add_node]['state']
            else:
                res[key]['state'] = 'UNKNOWN'
        with self.app.test_request_context():
            self.socketio.emit('my nodes response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Nodes event :%s' % (self.nodes))

    self.emit_nodes = emit_nodes


    def emit_node(nodes):
        """Emit a node state event
        nodes : a single node or a dict of nodes
        """
        #~ print " emit_node %s" %nodes
        #~ if 'hadd' not in nodes:
            #~ print " emit_node hadd not in nodes"
            #~ for key in nodes:
                #~ nodes[key]['state'] = 'online'
        with self.app.test_request_context():
            self.socketio.emit('my node response',
                {'data':nodes},
                namespace='/janitoo')
            logger.debug('Node event :%s' % (nodes))

    self.emit_node = emit_node


    def emit_users():
        """Emit a users state event
        """
        for hadd in self.users.keys():
            self.emit_user(self.users[hadd])

    self.emit_users = emit_users


    def emit_user(data):
        """Emit a usere state event
        nodes : a single node or a dict of nodes
        """
        res = {}
        i = 0
        if 'uuid' in data:
            data = {0:data}
        if 'uuid' in data[data.keys()[0]]:
            data = {0:data}
        for idx1 in data:
            #~ logger.debug('User event idx1 :%s,%s' % (idx1,data[idx1]))
            if idx1 not in res:
                res[idx1]={}
            for idx2 in data[idx1]:
                #~ logger.debug('User event idx2 :%s,%s' % (idx2,data[idx1][idx2]))
                res[idx1][idx2] = data[idx1][idx2]
        logger.debug('User event :%s' % (res))
        with self.app.test_request_context():
            self.socketio.emit('my users response',
                {'data':res},
                namespace='/janitoo')

    self.emit_user = emit_user


    def emit_basic(data):
        """Emit a basice state event
        nodes : a single node or a dict of nodes
        """
        res = {}
        i = 0
        if 'uuid' in data:
            data = {0:data}
        if 'uuid' in data[data.keys()[0]]:
            data = {0:data}
        for idx1 in data:
            #~ logger.debug('Basic event idx1 :%s,%s' % (idx1,data[idx1]))
            if idx1 not in res:
                res[idx1]={}
            for idx2 in data[idx1]:
                #~ logger.debug('Basic event idx2 :%s,%s' % (idx2,data[idx1][idx2]))
                res[idx1][idx2] = data[idx1][idx2]
        logger.debug('Basic event :%s' % (res))
        with self.app.test_request_context():
            self.socketio.emit('my basics response',
                {'data':res},
                namespace='/janitoo')

    self.emit_basic = emit_basic


    def emit_basics():
        """Emit a basics state event
        """
        for hadd in self.basics.keys():
            self.emit_basic(self.basics[hadd])
            #~ logger.debug('Values event :%s' % (self.basics))

    self.emit_basics = emit_basics

    def emit_system(data):
        """Emit a systeme state event
        nodes : a single node or a dict of nodes
        """
        res = {}
        i = 0
        if 'uuid' in data:
            data = {0:data}
        if 'uuid' in data[data.keys()[0]]:
            data = {0:data}
        for idx1 in data:
            logger.debug('System event idx1 :%s,%s' % (idx1,data[idx1]))
            if idx1 not in res:
                res[idx1]={}
            for idx2 in data[idx1]:
                logger.debug('System event idx2 :%s,%s' % (idx2,data[idx1][idx2]))
                res[idx1][idx2] = data[idx1][idx2]
        logger.debug('System event :%s' % (res))
        with self.app.test_request_context():
            self.socketio.emit('my systems response',
                {'data':res},
                namespace='/janitoo')

    self.emit_system = emit_system

    def emit_systems():
        """Emit a systems state event
        """
        for hadd in self.systems.keys():
            data = {}
            data.update(self.systems[hadd])
            self.emit_system(data)

    self.emit_systems = emit_systems

    def emit_commands():
        """Emit a commands state event
        """
        for hadd in self.commands.keys():
            self.emit_command(self.commands[hadd])

    self.emit_commands = emit_commands


    def emit_command(data):
        """Emit a commande state event
        nodes : a single node or a dict of nodes
        """
        res = {}
        i = 0
        if 'uuid' in data:
            data = {0:data}
        if 'uuid' in data[data.keys()[0]]:
            data = {0:data}
        for idx1 in data:
            #~ logger.debug('Command event idx1 :%s,%s' % (idx1,data[idx1]))
            if idx1 not in res:
                res[idx1]={}
            for idx2 in data[idx1]:
                #~ logger.debug('Command event idx2 :%s,%s' % (idx2,data[idx1][idx2]))
                res[idx1][idx1] = data[idx1][idx2]
        logger.debug('Command event :%s' % (res))
        with self.app.test_request_context():
            self.socketio.emit('my commands response',
                {'data':res},
                namespace='/janitoo')

    self.emit_command = emit_command

    def emit_scene(scenes):
        """Emit a scene state event
        nodes : a single scene or a dict of scenes
        """
        logger.debug('Value event :%s' % (scenes))

    self.emit_scene = emit_scene

    def emit_scenes():
        """Emit a scene state event
        """
        res = {}
        res.update(self.get_scenes())
        with self.app.test_request_context():
            self.socketio.emit('my scenes response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (res))

    self.emit_scenes = emit_scenes

    def emit_scenario(scenarios):
        """Emit a scenario state event
        nodes : a single scenario or a dict of scenarios
        """
        logger.debug('Value event :%s' % (scenarios))

    self.emit_scenario = emit_scenario

    def emit_scenarios():
        """Emit a scenario state event
        """
        res = {}
        res.update(self.get_scenarios())
        with self.app.test_request_context():
            self.socketio.emit('my scenarios response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (res))

    self.emit_scenarios = emit_scenarios

    def emit_cron(crons):
        """Emit a cron state event
        nodes : a single cron or a dict of crons
        """
        logger.debug('Value event :%s' % (crons))

    self.emit_cron = emit_cron

    def emit_crons():
        """Emit a cron state event
        """
        res = {}
        res.update(self.get_crons())
        with self.app.test_request_context():
            self.socketio.emit('my crons response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (res))

    self.emit_crons = emit_crons

    def emit_configs():
        """Emit a configs state event
        """
        for hadd in self.configs.keys():
            self.emit_config(self.configs[hadd])

    self.emit_configs = emit_configs


    def emit_config(data):
        """Emit a config state event
        nodes : a single node or a dict of nodes
        """
        res = {}
        i = 0
        if 'uuid' in data:
            data = {0:data}
        if 'uuid' in data[data.keys()[0]]:
            data = {0:data}
        for idx1 in data:
            #~ logger.debug('Config event idx1 :%s,%s' % (idx1,data[idx1]))
            if idx1 not in res:
                res[idx1]={}
            for idx2 in data[idx1]:
                #~ logger.debug('Config event idx2 :%s,%s' % (idx2,data[idx1][idx2]))
                res[idx1][idx2] = data[idx1][idx2]
        logger.debug('Config event :%s' % (res))
        with self.app.test_request_context():
            self.socketio.emit('my configs response',
                {'data':res},
                namespace='/janitoo')


    self.emit_config = emit_config
