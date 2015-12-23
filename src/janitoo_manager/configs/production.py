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


from janitoo_flask.options import OptionsConfig

class ProductionConfig(OptionsConfig):

    # Indicates that it is a dev environment
    #DEBUG = True

    # This will print all SQL statements
    #SQLALCHEMY_ECHO = True

    # Security
    SECRET_KEY = "SecretKeyForSessionSigning"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # Recaptcha
    # To get recaptcha, visit the link below:
    # https://www.google.com/recaptcha/admin/create
    # Those keys are only going to work on localhost!
    RECAPTCHA_ENABLED = True
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "6LcZB-0SAAAAAGIddBuSFU9aBpHKDa16p5gSqnxK"
    RECAPTCHA_PRIVATE_KEY = "6LcZB-0SAAAAAPuPHhazscMJYa2mBe7MJSoWXrUu"
    RECAPTCHA_OPTIONS = {"theme": "white"}

    # Mail
    # Local SMTP Server
    #MAIL_SERVER = "localhost"
    #MAIL_PORT = 25
    #MAIL_USE_SSL = False
    #MAIL_USERNAME = ""
    #MAIL_PASSWORD = ""
    #MAIL_DEFAULT_SENDER = "noreply@example.org"

    # Google Mail Example
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "your_username@gmail.com"
    MAIL_PASSWORD = "your_password"
    MAIL_DEFAULT_SENDER = ("Your Name", "your_username@gmail.com")

    # The user who should recieve the error logs
    ADMINS = ["your_admin_user@gmail.com"]

    #DEBUG_TB_INTERCEPT_REDIRECTS = True

    # URL Prefixes
    USER_URL_PREFIX = "/user"
    AUTH_URL_PREFIX = "/auth"
    ADMIN_URL_PREFIX = "/admin"
    PORTAL_URL_PREFIX = "/"

    def __init__(self, conf_file='/opt/janitoo/etc/janitoo_manager.conf'):
        """Update Flask default data from janitoo option file
        """
        OptionsConfig.__init__(self, conf_file)
