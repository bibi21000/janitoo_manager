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

def check_perm(user, perm, forum, post_user_id=None):
    """Checks if the `user` has a specified `perm` in the `forum`
    If post_user_id is provided, it will also check if the user
    has created the post

    :param user: The user for whom we should check the permission

    :param perm: The permission. You can find a full list of available
                 permissions here: <INSERT LINK TO DOCS>

    :param forum: The forum where we should check the permission against

    :param post_user_id: If post_user_id is given, it will also perform an
                         check if the user is the owner of this topic or post.
    """
    if can_moderate(user=user, forum=forum):
        return True

    if post_user_id and user.is_authenticated():
        return user.permissions[perm] and user.id == post_user_id

    return not user.permissions['banned'] and user.permissions[perm]


def is_power(user):
    """Returns ``True`` if the user is in a moderator or super moderator group.

    :param user: The user who should be checked.
    """
    return user.permissions['power']


def is_admin(user):
    """Returns ``True`` if the user is a administrator.

    :param user:  The user who should be checked.
    """
    return user.permissions['admin']


def is_admin_or_power(user):
    """Returns ``True`` if the user is either a admin or in a moderator group

    :param user: The user who should be checked.
    """
    return is_admin(user) or is_power(user)


def can_moderate(user, forum=None, perm=None):
    """Checks if a user can moderate a forum or a user.
    He needs to be super moderator or a moderator of the
    specified forum.

    :param user: The user for whom we should check the permission.

    :param forum: The forum that should be checked. If no forum is specified
                  it will check if the user has at least moderator permissions
                  and then it will perform another permission check for ``mod``
                  permissions (they start with ``mod_``).

    :param perm: Optional - Check if the user also has the permission to do
                 certain things in the forum. There are a few permissions
                 where you need to be at least a moderator (or anything higher)
                 in the forum and therefore you can pass a permission and
                 it will check if the user has it. Those special permissions
                 are documented here: <INSERT LINK TO DOCS>
    """
    # Check if the user has moderator specific permissions (mod_ prefix)
    if is_admin_or_moderator(user) and forum is None:

        if perm is not None and perm.startswith("mod_"):
            return user.permissions[perm]

        # If no permission is definied, return False
        return False

    # check if the user is a moderation and is moderating the forum
    if user.permissions['mod'] and user in forum.moderators:
        return True

    # if the user is a super_mod or admin, he can moderate all forums
    return user.permissions['super_mod'] or user.permissions['admin']


def can_edit_post(user, post):
    """Check if the post can be edited by the user."""
    topic = post.topic

    if can_moderate(user, topic.forum):
        return True

    if topic.locked or topic.forum.locked:
        return False

    return check_perm(user=user, perm='editpost', forum=post.topic.forum,
                      post_user_id=post.user_id)


def can_delete_post(user, post):
    """Check if the post can be deleted by the user."""
    return check_perm(user=user, perm='deletepost', forum=post.topic.forum,
                      post_user_id=post.user_id)


def can_delete_topic(user, topic):
    """Check if the topic can be deleted by the user."""
    return check_perm(user=user, perm='deletetopic', forum=topic.forum,
                      post_user_id=topic.user_id)


def can_post_reply(user, topic):
    """Check if the user is allowed to post in the forum."""
    if can_moderate(user, topic.forum):
        return True

    if topic.locked or topic.forum.locked:
        return False

    return check_perm(user=user, perm='postreply', forum=topic.forum)


def can_post_topic(user, forum):
    """Checks if the user is allowed to create a new topic in the forum."""
    return check_perm(user=user, perm='posttopic', forum=forum)


# Moderator permission checks
def can_edit_user(user):
    """Check if the user is allowed to edit another users profile.
    Requires at least ``mod`` permissions.
    """
    return can_moderate(user=user, perm="mod_edituser")


def can_ban_user(user):
    """Check if the user is allowed to ban another user.
    Requires at least ``mod`` permissions.
    """
    return can_moderate(user=user, perm="mod_banuser")
