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

from wtforms import (TextField, IntegerField, FloatField, BooleanField,
                     SelectField, SelectMultipleField, validators)
from flask_wtf import Form

from janitoo_manager._compat import max_integer, text_type, iteritems
from janitoo_manager.extensions import db, cache
from janitoo_manager.utils.database import CRUDMixin

import janitoo_db.models as jnt_models

class SettingGroupMan(jnt_models.SettingGroup, db.Model):
    pass

class SettingMan(jnt_models.Setting, db.Model):

    @classmethod
    def get_form(cls, group):
        """Returns a Form for all settings found in :class:`SettingsGroup`.

        :param group: The settingsgroup name. It is used to get the settings
                      which are in the specified group.
        """

        class SettingsForm(Form):
            pass

        # now parse the settings in this group
        for setting in group.settings:
            field_validators = []

            if setting.value_type in ("integer", "float"):
                validator_class = validators.NumberRange
            elif setting.value_type == "string":
                validator_class = validators.Length

            # generate the validators
            if "min" in setting.extra:
                # Min number validator
                field_validators.append(
                    validator_class(min=setting.extra["min"])
                )

            if "max" in setting.extra:
                # Max number validator
                field_validators.append(
                    validator_class(max=setting.extra["max"])
                )

            # Generate the fields based on value_type
            # IntegerField
            if setting.value_type == "integer":
                setattr(
                    SettingsForm, setting.key,
                    IntegerField(setting.name, validators=field_validators,
                                 description=setting.description)
                )
            # FloatField
            elif setting.value_type == "float":
                setattr(
                    SettingsForm, setting.key,
                    FloatField(setting.name, validators=field_validators,
                               description=setting.description)
                )

            # TextField
            elif setting.value_type == "string":
                setattr(
                    SettingsForm, setting.key,
                    TextField(setting.name, validators=field_validators,
                              description=setting.description)
                )

            # SelectMultipleField
            elif setting.value_type == "selectmultiple":
                # if no coerce is found, it will fallback to unicode
                if "coerce" in setting.extra:
                    coerce_to = setting.extra['coerce']
                else:
                    coerce_to = text_type

                setattr(
                    SettingsForm, setting.key,
                    SelectMultipleField(
                        setting.name,
                        choices=setting.extra['choices'](),
                        coerce=coerce_to,
                        description=setting.description
                    )
                )

            # SelectField
            elif setting.value_type == "select":
                # if no coerce is found, it will fallback to unicode
                if "coerce" in setting.extra:
                    coerce_to = setting.extra['coerce']
                else:
                    coerce_to = text_type

                setattr(
                    SettingsForm, setting.key,
                    SelectField(
                        setting.name,
                        coerce=coerce_to,
                        choices=setting.extra['choices'](),
                        description=setting.description)
                )

            # BooleanField
            elif setting.value_type == "boolean":
                setattr(
                    SettingsForm, setting.key,
                    BooleanField(setting.name, description=setting.description)
                )

        return SettingsForm

    #~ @classmethod
    #~ @cache.memoize(timeout=max_integer)
    #~ def as_dict(cls, from_group=None, upper=True):
        #~ """Returns all settings as a dict. This method is cached. If you want
        #~ to invalidate the cache, simply execute ``self.invalidate_cache()``.
#~
        #~ :param from_group: Returns only the settings from the group as a dict.
        #~ :param upper: If upper is ``True``, the key will use upper-case
                      #~ letters. Defaults to ``False``.
        #~ """
        #~ return jnt_models.Setting.as_dict(cls, from_group, upper)

    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""
        cache.delete_memoized(cls.as_dict, cls)
