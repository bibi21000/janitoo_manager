# -*- coding: utf-8 -*-

"""The network socket

Thinking about rooms.
- A room for the network : state,
- A room for nodes : list, add, remove, ...
- A room for each nodes (nodeid_1): values, parameters, ...
- A room for the controller
- A room for values

When joining a room, you will receive message from it.



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

    Original copyright :
    Copyright (c) 2013 Roger Light <roger@atchoo.org>

    All rights reserved. This program and the accompanying materials
    are made available under the terms of the Eclipse Distribution License v1.0
    which accompanies this distribution.

    The Eclipse Distribution License is available at
    http://www.eclipse.org/org/documents/edl-v10.php.

    Contributors:
     - Roger Light - initial implementation

    This example shows how you can use the MQTT client in a class.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"
#~ from gevent import monkey
#~ monkey.patch_all()

import logging
logger = logging.getLogger(__name__)
import os, sys
import time
from threading import Thread

from flask import Flask, render_template, session, request, current_app
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

from janitoo_manager.extensions import socketio, janitoo

@socketio.on('my echo event', namespace='/janitoo')
def echo_message(message):
    logger.debug("Client %s request echo message : %s", request.remote_addr, message)
    emit('my response',
         {'data': message['data']})

@socketio.on('disconnect request', namespace='/janitoo')
def disconnect_request():
    logger.debug("Client %s disconnects", request.remote_addr)
    emit('my response',
         {'data': 'Disconnected!'})
    disconnect()

@socketio.on('connect', namespace='/janitoo')
def echo_connect():
    logger.debug("Client %s connects", request.remote_addr)
    emit('my response', {'data': 'Connected'})

@socketio.on('my network event', namespace='/janitoo')
def echo_network_event(message):
    logger.debug("Client %s network event : %s", request.remote_addr, message)
    done=False
    keys = ['zoomlevel','zoomx','zoomy','panx','pany']
    kvals = {}
    for key in keys:
        if key in message:
            kvals[key]=message[key]
    logger.debug("kvals : %s", kvals)
    if len(kvals) > 0:
        janitoo.listener.network.kvals = kvals
        done = True
        #Should we emit an event ? Or the api should send a new python louie mesage ? Or nothing
    if done == False :
        janitoo.listener.network.emit_network()

@socketio.on('my node event', namespace='/janitoo')
def echo_node_event(message):
    logger.debug("Client %s node event : %s", request.remote_addr, message)
    try :
        node_id = int(message['node_id'])
    except ValueError:
        node_id = 0
    except KeyError:
        node_id = 0
    if node_id == 0 or node_id not in current_app.extensions['zwnetwork'].nodes:
        logger.warning('Received invalid node_id : %s', message)
        return
    done=False
    keys = ['posx','posy']
    kvals = {}
    for key in keys:
        if key in message:
            kvals[key]=message[key]
    logger.debug("kvals : %s", kvals)
    if len(kvals) > 0:
        current_app.extensions['zwnetwork'].nodes[node_id].kvals = kvals
        done = True
        #Should we emit an event ? Or the api should send a new python louie mesage ? Or nothing
    if 'name' in message:
        current_app.extensions['zwnetwork'].nodes[node_id].name = message['name']
        done = True
    if 'location' in message:
        current_app.extensions['zwnetwork'].nodes[node_id].location = message['location']
        done = True
    if done == False :
        logger.debug("Client %s node event : emit my node response")
        emit('my node response',
             {'data': current_app.extensions['zwnetwork'].nodes[node_id].to_dict()})

@socketio.on('my nodes event', namespace='/janitoo')
def echo_nodes_event(message):
    logger.debug("Client %s nodes event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_nodes()

@socketio.on('my controller event', namespace='/janitoo')
def echo_controller_event(message):
    logger.debug("Client %s controller event : %s", request.remote_addr, message)
    emit('my controller response',
         {'data': janitoo.listener.network.nodes})

@socketio.on('my command event', namespace='/janitoo')
def echo_command_event(message):
    logger.debug("Client %s controller command event : %s", request.remote_addr, message)
    data = {}
    data['result'] = False
    data['message'] = "Command fail to start"
    command = message['command']
    init_data = {'result':False, 'message':'', 'state':'', 'command':command}
    #Emit a blank message to clean the old data in javascript
    emit('my command response',
        {'data': init_data,
        })
    if command == 'no_command':
        #This is for first time launch. Return default values for javascript
        data = {}
        data['message'] = current_app.extensions['zwnetwork'].controller.ctrl_last_message
        data['state'] = current_app.extensions['zwnetwork'].controller.ctrl_last_state
        emit('my message response',
            {'data': data,})
        emit('my command response',
            {'data': init_data,})
        return
    elif command == 'send_node_information':
        node_id=-1
        try:
            node_id=int(message['node_id'])
        except ValueError:
            node_id = -1
        except KeyError:
            node_id = -1
        if node_id not in current_app.extensions['zwnetwork'].nodes :
            data['result'] = False
            data['message'] = "Bad node_id"
        else:
            data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_send_node_information(node_id)
            #data['result'] = True
    elif command == 'remove_failed_node':
        node_id=-1
        try:
            node_id=int(message['node_id'])
        except ValueError:
            node_id = -1
        except KeyError:
            node_id = -1
        if node_id not in current_app.extensions['zwnetwork'].nodes :
            data['result'] = False
            data['message'] = "Bad node_id"
        else:
            data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_remove_failed_node(node_id)
            #data['result'] = True
    elif command == 'has_node_failed':
        node_id=-1
        try:
            node_id=int(message['node_id'])
        except ValueError:
            node_id = -1
        except KeyError:
            node_id = -1
        if node_id not in current_app.extensions['zwnetwork'].nodes :
            data['result'] = False
            data['message'] = "Bad node_id"
        else:
            data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_has_node_failed(node_id)
            #data['result'] = True
    elif command == 'replace_failed_node':
        node_id=-1
        try:
            node_id=int(message['node_id'])
        except ValueError:
            node_id = -1
        except KeyError:
            node_id = -1
        if node_id not in current_app.extensions['zwnetwork'].nodes :
            data['result'] = False
            data['message'] = "Bad node_id"
        else:
            data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_replace_failed_node(node_id)
            #data['result'] = True
    elif command == 'request_node_neigbhor_update':
        node_id=-1
        try:
            node_id=int(message['node_id'])
        except ValueError:
            node_id = -1
        except KeyError:
            node_id = -1
        if node_id not in current_app.extensions['zwnetwork'].nodes :
            data['result'] = False
            data['message'] = "Bad node_id"
        else:
            data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_request_node_neigbhor_update(node_id)
            #data['result'] = True
    elif command == 'request_network_update':
        data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_request_network_update()
    elif command == 'replication_send':
        try:
            high_power = bool(message['high_power']) if 'high_power' in message else False
        except ValueError:
            high_power = False
        except KeyError:
            high_power = False
        data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_replication_send(high_power)
        #data['result'] = True
    elif command == 'add_device':
        try:
            high_power = bool(message['high_power']) if 'high_power' in message else False
        except ValueError:
            high_power = False
        except KeyError:
            high_power = False
        data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_add_device(high_power)
        #data['result'] = True
    elif command == 'remove_device':
        try:
            high_power = bool(message['high_power']) if 'high_power' in message else False
        except ValueError:
            high_power = False
        except KeyError:
            high_power = False
        data['result'] = current_app.extensions['zwnetwork'].controller.begin_command_remove_device(high_power)
        #data['result'] = True
    elif command == 'cancel_command':
        data['result'] = current_app.extensions['zwnetwork'].controller.cancel_command()
    if data['result'] == True :
        data['message'] = "Command started"
    logger.debug("Client %s controller command event, data returned : %s", request.remote_addr, data)
    emit('my command response',
         {'data': data,
          'count': session['receive_count']})

@socketio.on('my commands event', namespace='/janitoo')
def echo_commands_event(message):
    logger.debug("Client %s commands event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_commands()

@socketio.on('my user event', namespace='/janitoo')
def echo_user_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    node_id = message['hadd']
    user_id = message['uuid']
    logger.debug("Client %s user event : %s", request.remote_addr, janitoo.listener.users_count)
    #~ emit('my user response',
         #~ {'data': current_app.extensions['zwnetwork'].nodes[node_id].users[user_id].to_dict(), 'count': session['receive_count']})

@socketio.on('my users event', namespace='/janitoo')
def echo_users_event(message):
    logger.debug("Client %s users event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_users()

@socketio.on('my system event', namespace='/janitoo')
def echo_system_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    node_id = message['hadd']
    system_id = message['uuid']
    logger.debug("Client %s system event : %s", request.remote_addr, janitoo.listener.systems_count)
    #~ emit('my system response',
         #~ {'data': current_app.extensions['zwnetwork'].nodes[node_id].systems[system_id].to_dict(), 'count': session['receive_count']})

@socketio.on('my systems event', namespace='/janitoo')
def echo_systems_event(message):
    logger.debug("Client %s systems event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_systems()

@socketio.on('my basic event', namespace='/janitoo')
def echo_basic_event(message):
    node_id = message['hadd']
    basic_id = message['uuid']
    logger.debug("Client %s basic event : %s", request.remote_addr, janitoo.listener.basics_count)
    #~ emit('my basic response',
         #~ {'data': current_app.extensions['zwnetwork'].nodes[node_id].basics[basic_id].to_dict(), 'count': session['receive_count']})

@socketio.on('my basics event', namespace='/janitoo')
def echo_basics_event(message):
    logger.debug("Client %s basics event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_basics()

@socketio.on('my config event', namespace='/janitoo')
def echo_config_event(message):
    node_id = message['hadd']
    value_id = message['uuid']
    logger.debug("Client %s config event : %s", request.remote_addr, janitoo.listener.configs_count)
    #~ emit('my value response',
         #~ {'data': current_app.extensions['zwnetwork'].nodes[node_id].values[value_id].to_dict(), 'count': session['receive_count']})

@socketio.on('my configs event', namespace='/janitoo')
def echo_configs_event(message):
    logger.debug("Client %s emit_configs event : %s", request.remote_addr, message)
    #print "%s"%current_app.extensions['zwnetwork'].nodes_to_dict()
    janitoo.listener.network.emit_configs()

@socketio.on('my scenes event', namespace='/janitoo')
def echo_scenes_event(message):
    logger.debug("Client %s scenes event : %s", request.remote_addr, message)
    print "get_scenes %s"%janitoo.listener.network.get_scenes()
    emit('my scenes response',
         {'data': janitoo.listener.network.get_scenes()})

@socketio.on('my scenarios event', namespace='/janitoo')
def echo_scenarios_event(message):
    logger.debug("Client %s scenarios event : %s", request.remote_addr, message)
    print "get_scenarios %s"%janitoo.listener.network.get_scenarios()
    emit('my scenarios response',
         {'data': janitoo.listener.network.get_scenarios()})

@socketio.on('my crons event', namespace='/janitoo')
def echo_crons_event(message):
    logger.debug("Client %s crons event : %s", request.remote_addr, message)
    print "get_crons %s"%janitoo.listener.network.get_crons()
    emit('my crons response',
         {'data': janitoo.listener.network.get_crons()})

