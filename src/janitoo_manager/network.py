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
        res = {}
        i = 0
        #~ print "self.ussssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssers", self.users
        for hadd in self.users:
            if hadd not in res:
                res[hadd]={}
            for uuid in self.users[hadd]:
                for index in self.users[hadd][uuid]:
                    #~ print 'emit_users', hadd, uuid, index
                    res[hadd][i] = self.users[hadd][uuid][index]
                    i += 1
        #~ print "emiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit users", res
        with self.app.test_request_context():
            self.socketio.emit('my users response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (self.users))

    self.emit_users = emit_users


    def emit_user(nodes):
        """Emit a usere state event
        nodes : a single node or a dict of nodes
        """
        logger.debug('Value event :%s' % (nodes))

    self.emit_user = emit_user


    def emit_basic(nodes):
        """Emit a basice state event
        nodes : a single node or a dict of nodes
        """
        logger.debug('Value event :%s' % (nodes))

    self.emit_basic = emit_basic


    def emit_basics():
        """Emit a basics state event
        """
        res = {}
        i = 0
        #~ print "emit_basics", self.basics
        for hadd in self.basics:
            if hadd not in res:
                res[hadd]={}
            for uuid in self.basics[hadd]:
                for index in self.basics[hadd][uuid]:
                    #~ print 'emit_basics', hadd, uuid, index
                    res[hadd][i] = self.basics[hadd][uuid][index]
                    i += 1
        #~ print "emiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit basics", res
        with self.app.test_request_context():
            self.socketio.emit('my basics response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (self.basics))

    self.emit_basics = emit_basics

    def emit_system(nodes):
        """Emit a systeme state event
        nodes : a single node or a dict of nodes
        """
        logger.debug('Value event :%s' % (nodes))

    self.emit_system = emit_system

    def emit_systems():
        """Emit a systems state event
        """
        res = {}
        res.update(self.systems)
        with self.app.test_request_context():
            self.socketio.emit('my systems response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (self.systems))

    self.emit_systems = emit_systems

    def emit_command(nodes):
        """Emit a command state event
        nodes : a single node or a dict of nodes
        """
        logger.debug('Value event :%s' % (nodes))

    self.emit_command = emit_command

    def emit_commands():
        """Emit a systems state event
        """
        res = {}
        res.update(self.commands)
        with self.app.test_request_context():
            self.socketio.emit('my commands response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Values event :%s' % (self.commands))

    self.emit_commands = emit_commands

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
        res = {}
        i = 0
        #~ print "self.confis", self.configs
        for hadd in self.configs:
            if hadd not in res:
                res[hadd]={}
            for uuid in self.configs[hadd]:
                for index in self.configs[hadd][uuid]:
                    #~ print 'emit_configs', hadd, uuid, index
                    res[hadd][i] = self.configs[hadd][uuid][index]
                    i += 1
        #~ print "emiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit configs", res
        with self.app.test_request_context():
            self.socketio.emit('my configs response',
                {'data':res},
                namespace='/janitoo')
            logger.debug('Configs event :%s' % (self.configs))

    self.emit_configs = emit_configs


    def emit_config(nodes):
        """Emit a config state event
        nodes : a single node or a dict of nodes
        """
        logger.debug('Config event :%s' % (nodes))

    self.emit_config = emit_config
