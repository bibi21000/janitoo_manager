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
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"
#~ from gevent import monkey
#~ monkey.patch_all()

import logging
logger = logging.getLogger(__name__)

from flask import Blueprint, flash, request
from flask_login import login_required, current_user
from flask_themes2 import get_themes_list
from flask_babelplus import gettext as _

from janitoo.classes import CAPABILITY_DESC, GENRE_DESC, VALUE_DESC, COMMAND_DESC

from janitoo_manager.extensions import babel, cache, janitoo
from janitoo_manager.utils.helpers import render_template
from janitoo_manager.user.models import UserMan

portal = Blueprint("portal", __name__)

@portal.before_request
def start_listener():
    janitoo.start_listener()

@portal.route("")
def index():
    """
    """
    return render_template("portal/index.html", user=current_user)

@cache.cached(timeout=900)
@portal.route('janitoo_constants.js')
def janitoo_constants_js():
    return render_template('janitoo_constants.js', capabilities=CAPABILITY_DESC, genres=GENRE_DESC, values=VALUE_DESC, commands=COMMAND_DESC)
