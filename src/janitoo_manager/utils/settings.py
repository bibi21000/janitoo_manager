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
#~ from gevent import monkey
#~ monkey.patch_all()

import logging
logger = logging.getLogger(__name__)

import collections

from janitoo_manager.management.models import SettingMan
#~ import janitoo_db.models as jnt_models

class ManagerConfig(collections.MutableMapping):
    """Provides a dictionary like interface for interacting with janitoo_manager's
    Settings cache.
    """

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return SettingMan.as_dict()[key]

    def __setitem__(self, key, value):
        SettingMan.update({key.lower(): value})

    def __delitem__(self, key):  # pragma: no cover
        pass

    def __iter__(self):
        return iter(SettingMan.as_dict())

    def __len__(self):
        return len(SettingMan.as_dict())

flask_config = ManagerConfig()
