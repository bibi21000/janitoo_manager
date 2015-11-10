# -*- coding: utf-8 -*-
"""
    janitoo_manager.fixtures.groups
    ~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our groups.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict


fixture = OrderedDict((
    ('Administrator', {
        'description': 'The Administrator Group',
        'admin': True,
        'power': False,
        'user': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
    }),
    ('Power User', {
        'description': 'The Power User Group',
        'admin': False,
        'power': True,
        'user': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
    }),
    ('User', {
        'description': 'The User Group',
        'admin': False,
        'power': False,
        'user': True,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
    }),
    ('Member', {
        'description': 'The Member Group',
        'admin': False,
        'power': False,
        'user': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': False,
        'mod_banuser': False,
    }),
    ('Banned', {
        'description': 'The Banned Group',
        'admin': False,
        'power': False,
        'user': False,
        'banned': True,
        'guest': False,
        'editpost': False,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': False,
        'postreply': False,
        'mod_edituser': False,
        'mod_banuser': False,
    }),
    ('Guest', {
        'description': 'The Guest Group',
        'admin': False,
        'power': False,
        'user': False,
        'banned': False,
        'guest': True,
        'editpost': False,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': False,
        'postreply': False,
        'mod_edituser': False,
        'mod_banuser': False,
    })
))
