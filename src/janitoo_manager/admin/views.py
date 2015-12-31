# -*- coding: utf-8 -*-

"""The main views

Thinking about rooms.
- A room for the network : state,
- A room for nodes : list, add, remove, ...
- A room for each nodes (nodeid_1): values, parameters, ...
- A room for the controller
- A room for values

When joining a room, you will receive message from it.

"""

__license__ = """

This file is part of **janitoo** project https://github.com/bibi21000/janitoo.

License : GPL(v3)

**janitoo** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**janitoo** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with janitoo. If not, see http://www.gnu.org/licenses.
"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
from gevent import monkey
monkey.patch_all()

import logging
logger = logging.getLogger(__name__)

import os, sys
import time
from threading import Thread

from flask import Blueprint, flash
from flask import Flask, session, request, current_app, g
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect
from flask_themes2 import get_themes_list
from flask_babelex import gettext as _

from janitoo_manager.extensions import babel, janitoo
from janitoo_manager.utils.helpers import render_template

#~ from janitoo_web.app import socketio, app, sort_application_entries, sorted_application_entries
#~ from janitoo_web.app.listener import listener


admin = Blueprint("admin", __name__)

@admin.before_request
def start_listener():
    janitoo.start_listener()

@admin.route('/')
@admin.route('/nodes')
def nodes():
    return render_template('admin/nodes.html')

@admin.route('/node')
@admin.route('/node/<int:ctrl_id>/<int:device_id>')
def node(ctrl_id=None, device_id=None):
    return render_template('node.html', ctrl_id=ctrl_id, device_id=device_id)

@admin.route('/scenes')
def scenes():
    return render_template('scenes.html')

@admin.route('/scene')
@admin.route('/scene/<int:ctrl_id>/<int:device_id>')
def scene(ctrl_id=None, device_id=None):
    return render_template('scene.html', ctrl_id=ctrl_id, device_id=device_id)

@admin.route('/scenarios')
def scenarios():
    return render_template('scenarios.html')

@admin.route('/scenario')
@admin.route('/scenario/<int:ctrl_id>/<int:device_id>')
def scenario(ctrl_id=None, device_id=None):
    return render_template('scenario.html', ctrl_id=ctrl_id, device_id=device_id)

@admin.route('/crons')
def crons():
    return render_template('crons.html')

@admin.route('/cron')
@admin.route('/cron/<int:ctrl_id>/<int:device_id>')
def cron(ctrl_id=None, device_id=None):
    return render_template('cron.html', ctrl_id=ctrl_id, device_id=device_id)

@admin.route('/values_user')
def values_user():
    return render_template('admin/values_user.html')

@admin.route('/values_config')
def values_config():
    return render_template('admin/values_config.html')

@admin.route('/values_command')
def values_command():
    return render_template('admin/values_command.html')

@admin.route('/values_system')
def values_system():
    return render_template('admin/values_system.html')

@admin.route('/values_basic')
def values_basic():
    return render_template('admin/values_basic.html')

@admin.route('/controller')
def controller():
    return render_template('controller.html')

@admin.route('/debug')
def debug():
    return render_template('debug.html')

@admin.route('/map')
def map():
    return render_template('map.html')

@admin.route('/chat')
def chat():
    return render_template('chat.html')
