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
logger = logging.getLogger('janitoo.manager')

from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_anonymous():
            abort(403)
        if not current_user.permissions['admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated


def moderator_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_anonymous():
            abort(403)

        if not any([current_user.permissions['admin'],
                    current_user.permissions['super_mod'],
                    current_user.permissions['mod']]):
            abort(403)

        return f(*args, **kwargs)
    return decorated


def can_access_forum(func):
    def decorated(*args, **kwargs):
        forum_id = kwargs['forum_id'] if 'forum_id' in kwargs else args[1]
        from janitoo_manager.forum.models import Forum
        from janitoo_manager.user.models import Group

        # get list of user group ids
        if current_user.is_authenticated():
            user_groups = [gr.id for gr in current_user.groups]
        else:
            user_groups = [Group.get_guest_group().id]

        user_forums = Forum.query.filter(
            Forum.id == forum_id, Forum.groups.any(Group.id.in_(user_groups))
        ).all()

        if len(user_forums) < 1:
            abort(403)

        return func(*args, **kwargs)
    return decorated


def can_access_topic(func):
    def decorated(*args, **kwargs):
        topic_id = kwargs['topic_id'] if 'topic_id' in kwargs else args[1]
        from janitoo_manager.forum.models import Forum, Topic
        from janitoo_manager.user.models import Group

        topic = Topic.query.filter_by(id=topic_id).first()
        # get list of user group ids
        if current_user.is_authenticated():
            user_groups = [gr.id for gr in current_user.groups]
        else:
            user_groups = [Group.get_guest_group().id]

        user_forums = Forum.query.filter(
            Forum.id == topic.forum.id,
            Forum.groups.any(Group.id.in_(user_groups))
        ).all()

        if len(user_forums) < 1:
            abort(403)

        return func(*args, **kwargs)
    return decorated
