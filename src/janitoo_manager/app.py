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
logger = logging.getLogger('janitoo.manager')

import os
import logging
logger = logging.getLogger("janitoo.manager")

import datetime
import time

from pkg_resources import iter_entry_points

from sqlalchemy import event
from sqlalchemy.engine import Engine

from flask import Flask, request
from flask_login import current_user

# Import the user blueprint
from janitoo_manager.admin.views import admin
from janitoo_manager.user.models import UserMan, GuestMan
from janitoo_manager.auth.views import auth
from janitoo_manager.user.views import user
from janitoo_manager.admin.views import admin
from janitoo_manager.portal.views import portal
from janitoo_manager.extensions import db, login_manager, mail, cache, janitoo, \
    debugtoolbar, plugin_manager, themes, babel, csrf, socketio, bower
# various helpers
from janitoo_manager.utils.helpers import format_date, time_since, crop_title, \
    is_online, render_markup, mark_online, forum_is_unread, topic_is_unread, \
    render_template
from janitoo_manager.utils.translations import JanitooDomain
# permission checks (here they are used for the jinja filters)
#~ from janitoo_manager.utils.permissions import can_post_reply, can_post_topic, \
    #~ can_delete_topic, can_delete_post, can_edit_post, can_edit_user, \
    #~ can_ban_user, can_moderate, is_admin, is_moderator, is_admin_or_moderator
from janitoo_manager.utils.permissions import is_admin, is_power, is_admin_or_power
# app specific configurations
from janitoo_manager.utils.settings import flask_config

#~ import janitoo_db.models as jnt_models
from janitoo_db.base import Base, create_db_engine
from janitoo_db.migrate import Config as alConfig, collect_configs, janitoo_config

def create_app(config=None):
    """Creates the app."""

    # Initialize the app
    app = Flask("janitoo_manager")

    # Use the default config and override it afterwards
    app.config.from_object('janitoo_flask.options.Config')
    # Update the config
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("JANITOO_SETTINGS", silent=True)

    configure_extensions(app)
    configure_blueprints(app)
    configure_template_filters(app)
    configure_context_processors(app)
    configure_before_handlers(app)
    configure_errorhandlers(app)
    configure_logging(app)

    return app


def configure_blueprints(app):
    app.register_blueprint(portal, url_prefix=app.config["PORTAL_URL_PREFIX"])
    app.register_blueprint(admin, url_prefix=app.config["ADMIN_URL_PREFIX"])
    app.register_blueprint(user, url_prefix=app.config["USER_URL_PREFIX"])
    app.register_blueprint(auth, url_prefix=app.config["AUTH_URL_PREFIX"])
    import janitoo_manager.admin.socket
    #~ from janitoo_manager_proxy.views import proxy
    #~ app.register_blueprint(proxy, url_prefix='/proxy')
    janitoo.extend_blueprints('janitoo_manager')

def configure_extensions(app):
    """Configures the extensions."""

    # Flask-WTF CSRF
    csrf.init_app(app)

    # Flask-Plugins
    plugin_manager.init_app(app)

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    #~ migrate.init_app(app, db, directory="config", filename="janitoo_manager.conf", section="database")

    # Flask-Mail
    mail.init_app(app)

    # Flask-Cache
    cache.init_app(app)

    # Flask-Bower
    bower.init_app(app)

    # Flask-Debugtoolbar
    debugtoolbar.init_app(app)

    # Flask-Themes
    themes.init_themes(app, app_identifier="janitoo_manager")

    # Flask-Login
    login_manager.login_view = app.config["LOGIN_VIEW"]
    login_manager.refresh_view = app.config["REAUTH_VIEW"]
    login_manager.anonymous_user = GuestMan

    @login_manager.user_loader
    def load_user(user_id):
        """Loads the user. Required by the `login` extension."""

        #~ unread_count = db.session.query(db.func.count(Conversation.id)).\
            #~ filter(Conversation.unread,
                   #~ Conversation.user_id == user_id).subquery()
        #~ u = db.session.query(User, unread_count).filter(User.id == user_id).\
            #~ first()
        u = db.session.query(UserMan).filter(UserMan.id == user_id).\
            first()

        if u:
            user_instance = u
            #~ user_instance, user_instance.pm_unread = u
            return user_instance
        else:
            return None

    login_manager.init_app(app)

    # Flask-BabelEx
    babel.init_app(app=app, default_domain=JanitooDomain(app))

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        if current_user.is_authenticated() and current_user.language:
            return current_user.language
        # otherwise we will just fallback to the default language
        print "============================>>>>>>>>>>>>>>>>>>>>> flask_config : %s" % flask_config
        return flask_config["DEFAULT_LANGUAGE"]

    # SocketIO
    socketio.init_app(app)

    # janitoo_flask
    janitoo.init_app(app, socketio, options={'conf_file':'/opt/janitoo/config/janitoo_manager.conf'}, db=db)
    janitoo.extend_network('janitoo_manager')
    janitoo.extend_listener('janitoo_manager')

def configure_template_filters(app):
    """Configures the template filters."""

    app.jinja_env.filters['markup'] = render_markup
    app.jinja_env.filters['format_date'] = format_date
    app.jinja_env.filters['time_since'] = time_since
    app.jinja_env.filters['is_online'] = is_online
    app.jinja_env.filters['crop_title'] = crop_title
    app.jinja_env.filters['forum_is_unread'] = forum_is_unread
    app.jinja_env.filters['topic_is_unread'] = topic_is_unread
    # Permission filters
    #~ app.jinja_env.filters['edit_post'] = can_edit_post
    #~ app.jinja_env.filters['delete_post'] = can_delete_post
    #~ app.jinja_env.filters['delete_topic'] = can_delete_topic
    #~ app.jinja_env.filters['post_reply'] = can_post_reply
    #~ app.jinja_env.filters['post_topic'] = can_post_topic
    # Moderator permission filters
    app.jinja_env.filters['is_admin'] = is_admin
    app.jinja_env.filters['is_power'] = is_power
    app.jinja_env.filters['is_admin_or_power'] = is_admin_or_power
    #~ app.jinja_env.filters['can_moderate'] = can_moderate
#~
    #~ app.jinja_env.filters['can_edit_user'] = can_edit_user
    #~ app.jinja_env.filters['can_ban_user'] = can_ban_user


def configure_context_processors(app):
    """Configures the context processors."""

    @app.context_processor
    def inject_janitoo_config():
        """Injects the ``flask_config`` config variable into the
        templates.
        """
        return dict(flask_config=flask_config)


def configure_before_handlers(app):
    """Configures the before request handlers."""

    @app.before_request
    def update_lastseen():
        """Updates `lastseen` before every reguest if the user is
        authenticated."""

        if current_user.is_authenticated():
            current_user.lastseen = datetime.datetime.utcnow()
            db.session.add(current_user)
            db.session.commit()

def configure_errorhandlers(app):
    """Configures the error handlers."""

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500


def configure_logging(app):
    """Configures logging."""

    #~ logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    #~ from logging.handlers import SMTPHandler
    #~ formatter = logging.Formatter(
        #~ '%(asctime)s %(levelname)s: %(message)s '
        #~ '[in %(pathname)s:%(lineno)d]')
#~
    #~ info_log = os.path.join(logs_folder, app.config['INFO_LOG'])
#~
    #~ info_file_handler = logging.handlers.RotatingFileHandler(
        #~ info_log,
        #~ maxBytes=100000,
        #~ backupCount=10
    #~ )
#~
    #~ info_file_handler.setLevel(logging.INFO)
    #~ info_file_handler.setFormatter(formatter)
    #~ app.logger.addHandler(info_file_handler)
#~
    #~ error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])
#~
    #~ error_file_handler = logging.handlers.RotatingFileHandler(
        #~ error_log,
        #~ maxBytes=100000,
        #~ backupCount=10
    #~ )
#~
    #~ error_file_handler.setLevel(logging.ERROR)
    #~ error_file_handler.setFormatter(formatter)
    #~ app.logger.addHandler(error_file_handler)
#~
    #~ if app.config["SEND_LOGS"]:
        #~ mail_handler = \
            #~ SMTPHandler(
                #~ app.config['MAIL_SERVER'],
                #~ app.config['MAIL_DEFAULT_SENDER'],
                #~ app.config['ADMINS'],
                #~ 'application error, no admins specified',
                #~ (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            #~ )
#~
        #~ mail_handler.setLevel(logging.ERROR)
        #~ mail_handler.setFormatter(formatter)
        #~ app.logger.addHandler(mail_handler)

    if app.config["SQLALCHEMY_ECHO"]:
        # Ref: http://stackoverflow.com/a/8428546
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement,
                                  parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time.time())

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement,
                                 parameters, context, executemany):
            total = time.time() - conn.info['query_start_time'].pop(-1)
            app.logger.debug("Total Time: %f", total)
