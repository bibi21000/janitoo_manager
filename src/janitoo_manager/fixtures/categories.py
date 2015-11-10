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
    (1, {
        u'title': u'International',
        u'description': u'International forum (English)',
        u'position': 1,
    }),
    (2, {
        u'title': u'Français',
        u'description': u'Le forum français',
        u'position': 2,
    }),
))
