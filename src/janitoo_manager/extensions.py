# -*- coding: utf-8 -*-
"""
    janitoo_manager.extensions
    ~~~~~~~~~~~~~~~~~~~~

    The extensions that are used by FlaskBB.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_themes2 import Themes
from flask_plugins import PluginManager
from flask_babelex import Babel
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
migrate = Migrate()

# Themes
themes = Themes()

# PluginManager
plugin_manager = PluginManager()

# Babel
babel = Babel()

# CSRF
csrf = CsrfProtect()

# SocketIO
socketio = SocketIO()

# flask_janitoo
janitoo = FlaskJanitoo()

def auth_func(*args, **kw):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not authenticated!', code=401)
