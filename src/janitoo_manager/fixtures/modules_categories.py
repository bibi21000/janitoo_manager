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
        u'title': u'Core',
        u'description': u'Core modules',
        u'position': 1,
    }),
    (2, {
        u'title': u'Protocols',
        u'description': u'Protocol modules',
        u'position': 2,
    }),
    (3, {
        u'title': u'Computers',
        u'description': u'Computers dédicated modules',
        u'position': 3,
    }),
))
