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

import os

import babel

from flask_babelplus import Domain, get_locale
#~ from flask_plugins import get_plugins_list

from janitoo_manager._compat import PY2


class JanitooDomain(Domain):
    def __init__(self, app):
        self.app = app
        super(JanitooDomain, self).__init__()

        #~ self.plugins_folder = os.path.join(
            #~ os.path.join(self.app.root_path, "plugins")
        #~ )

        # janitoo_manager's translations
        self.janitoo_manager_translations = os.path.join(
            self.app.root_path, "translations"
        )

        # Plugin translations
        #~ with self.app.app_context():
            #~ self.plugin_translations = [
                #~ os.path.join(plugin.path, "translations")
                #~ for plugin in get_plugins_list()
            #~ ]

    def get_translations(self):
        """Returns the correct gettext translations that should be used for
        this request.  This will never fail and return a dummy translation
        object if used outside of the request or if a translation cannot be
        found.
        """
        locale = get_locale()
        cache = self.get_translations_cache()

        translations = cache.get(str(locale))
        if translations is None:
            # load janitoo_manager translations
            translations = babel.support.Translations.load(
                dirname=self.janitoo_manager_translations,
                locales=locale,
                domain="messages"
            )

            # If no compiled translations are found, return the
            # NullTranslations object.
            if not isinstance(translations, babel.support.Translations):
                return translations

            # Plugin translations are at the moment not supported under
            # Python 3. There is currently a bug in Babel where it is
            # not possible to merge two message catalogs.
            # https://github.com/mitsuhiko/babel/pull/92
            # So instead of adding/merging them, we are just skipping them
            # Better then no python3 support though..
            if not PY2:
                return translations

            # now load and add the plugin translations
            #~ for plugin in self.plugin_translations:
                #~ plugin_translation = babel.support.Translations.load(
                    #~ dirname=plugin,
                    #~ locales=locale,
                    #~ domain="messages"
                #~ )
                #~ translations.add(plugin_translation)

            cache[str(locale)] = translations

        return translations
