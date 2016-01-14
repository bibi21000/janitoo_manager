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

from datetime import datetime
from wtforms.fields import DateField


class BirthdayField(DateField):
    """Same as DateField, except it allows ``None`` values in case a user
    wants to delete his birthday.
    """
    def __init__(self, label=None, validators=None, format='%Y-%m-%d',
                 **kwargs):
        DateField.__init__(self, label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist)
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None

                # Only except the None value if all values are None.
                # A bit dirty though
                if valuelist != ["None", "None", "None"]:
                    raise ValueError("Not a valid date value")
