# -*- coding: utf-8 -*-
"""
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
from gevent import monkey
monkey.patch_all()

import logging
logger = logging.getLogger(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
#~ from flask_migrate import Migrate
from flask_themes2 import Themes
from flask_plugins import PluginManager
from flask_babelex import Babel
from flask_bower import Bower
from flask_wtf.csrf import CsrfProtect
from janitoo_flask import FlaskJanitoo
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

# Database
db = SQLAlchemy()

# Login
login_manager = LoginManager()

# Caching
cache = Cache()

# Mail
mail = Mail()

# Debugtoolbar
debugtoolbar = DebugToolbarExtension()

# Migrations
#~ migrate = Migrate()

# Themes
themes = Themes()

# PluginManager
plugin_manager = PluginManager()

# Babel
babel = Babel()

# CSRF
csrf = CsrfProtect()

# Bower
bower = Bower()

# SocketIO
socketio = SocketIO()

# flask_janitoo
janitoo = FlaskJanitoo()

def auth_func(*args, **kw):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!', code=401)
