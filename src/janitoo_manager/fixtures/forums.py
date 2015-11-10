# -*- coding: utf-8 -*-
"""
    janitoo_manager.fixtures.categories
    ~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our groups.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict


fixture = OrderedDict((
    (u"News", {
        u'description': u"News from Janitoo core team",
        u'category_id': 1,
    }),
    (u"General use", {
        u'description': u"General use of Janitoo",
        u'category_id': 1,
    }),
    (u"Modules use", {
        u'description': u"Modules specific",
        u'category_id': 1,
    }),
    (u"Development", {
        u'description': u"For developpers",
        u'category_id': 1,
    }),
    (u"Annonces", {
        u'description': u"Annonces de l'équipe Janitoo",
        u'category_id': 2,
    }),
    (u"Utilisation générale", {
        u'description': u"Utilisation généralé de Janitoo",
        u'category_id': 2,
    }),
    (u"Utilisation des modules", {
        u'description': u"Utilisation des modules",
        u'category_id': 2,
    }),
    (u"Développement", {
        u'description': u"Pour les développeurs",
        u'category_id': 2,
    }),
))
