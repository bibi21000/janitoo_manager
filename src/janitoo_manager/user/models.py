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

from datetime import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin

from janitoo_manager._compat import max_integer
from janitoo_manager.extensions import db, cache
from janitoo_manager.utils.settings import flask_config
from janitoo_manager.utils.database import CRUDMixin

import janitoo_db.models as jnt_models

class GroupMan(jnt_models.Group, db.Model):
    pass

class UserMan(jnt_models.User, UserMixin, db.Model):

    @cache.memoize(timeout=max_integer)
    def get_groups(self):
        """Returns all the groups the user is in."""
        return jnt_models.User.get_groups(self)

    @cache.memoize(timeout=max_integer)
    def get_permissions(self, exclude=None):
        """Returns a dictionary with all the permissions the user has.

        :param exclude: a list with excluded permissions. default is None.
        """
        return jnt_models.User.get_permissions(self, exclude)

class GuestMan(AnonymousUserMixin):

    @cache.memoize(timeout=max_integer)
    def get_permissions(self, exclude=None):
        """Returns a dictionary with all permissions the user has"""
        return jnt_models.Guest.get_permissions(self, exclude)

    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""

        cache.delete_memoized(cls.get_permissions, cls)
