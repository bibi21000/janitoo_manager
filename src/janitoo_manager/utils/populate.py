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
from janitoo_manager.management.models import SettingMan, SettingGroupMan
from janitoo_manager.user.models import UserMan, GroupMan
#~ from janitoo_manager.forum.models import Post, Topic, Forum, Category
#~ from janitoo_manager.plugins.modules.models import Module, ModuleCategory
#~ import janitoo_db.models as jnt_models

def delete_settings_from_fixture(fixture):
    """Deletes the settings from a fixture from the database.
    Returns the deleted groups and settings.

    :param fixture: The fixture that should be deleted.
    """
    deleted_settings = {}

    for settingsgroup in fixture:
        group = SettingGroupMan.query.filter_by(key=settingsgroup[0]).first()
        deleted_settings[group] = []

        for settings in settingsgroup[1]["settings"]:
            setting = SettingMan.query.filter_by(key=settings[0]).first()
            if setting:
                deleted_settings[group].append(setting)
                setting.delete()

        group.delete()

    return deleted_settings


def create_settings_from_fixture(fixture):
    """Inserts the settings from a fixture into the database.
    Returns the created groups and settings.

    :param fixture: The fixture which should inserted.
    """
    created_settings = {}
    for settingsgroup in fixture:
        group = SettingGroupMan(
            key=settingsgroup[0],
            name=settingsgroup[1]["name"],
            description=settingsgroup[1]["description"]
        )
        group.save()
        created_settings[group] = []

        for settings in settingsgroup[1]["settings"]:
            setting = SettingMan(
                key=settings[0],
                value=settings[1]["value"],
                value_type=settings[1]["value_type"],
                name=settings[1]["name"],
                description=settings[1]["description"],
                extra=settings[1].get("extra", ""),     # Optional field

                settingsgroup=group.key
            )
            if setting:
                setting.save()
                created_settings[group].append(setting)

    return created_settings


def update_settings_from_fixture(fixture, overwrite_group=False,
                                 overwrite_setting=False):
    """Updates the database settings from a fixture.
    Returns the updated groups and settings.

    :param fixture: The fixture which should be inserted/updated.

    :param overwrite_group: Set this to ``True`` if you want to overwrite
                            the group if it already exists.
                            Defaults to ``False``.

    :param overwrite_setting: Set this to ``True`` if you want to overwrite the
                              setting if it already exists.
                              Defaults to ``False``.
    """
    updated_settings = {}

    for settingsgroup in fixture:

        group = SettingGroupMan.query.filter_by(key=settingsgroup[0]).first()

        if (group is not None and overwrite_group) or group is None:

            if group is not None:
                group.name = settingsgroup[1]["name"]
                group.description = settingsgroup[1]["description"]
            else:
                group = SettingGroupMan(
                    key=settingsgroup[0],
                    name=settingsgroup[1]["name"],
                    description=settingsgroup[1]["description"]
                )

            group.save()
            updated_settings[group] = []

        for settings in settingsgroup[1]["settings"]:

            setting = SettingMan.query.filter_by(key=settings[0]).first()

            if (setting is not None and overwrite_setting) or setting is None:

                if setting is not None:
                    setting.value = settings[1]["value"]
                    setting.value_type = settings[1]["value_type"]
                    setting.name = settings[1]["name"]
                    setting.description = settings[1]["description"]
                    setting.extra = settings[1].get("extra", "")
                    setting.settingsgroup = group.key
                else:
                    setting = SettingMan(
                        key=settings[0],
                        value=settings[1]["value"],
                        value_type=settings[1]["value_type"],
                        name=settings[1]["name"],
                        description=settings[1]["description"],
                        extra=settings[1].get("extra", ""),
                        settingsgroup=group.key
                    )

                setting.save()
                updated_settings[group].append(setting)

    return updated_settings


def create_default_settings():
    """Creates the default settings."""
    from janitoo_manager.fixtures.settings import fixture
    create_settings_from_fixture(fixture)


def create_default_groups():
    """This will create the 5 default groups."""
    from janitoo_manager.fixtures.groups import fixture
    result = []
    for key, value in fixture.items():
        group = Group(name=key)

        for k, v in value.items():
            setattr(group, k, v)

        group.save()
        result.append(group)
    return result

def create_default_categories():
    """This will create the 5 default groups."""
    from janitoo_manager.fixtures.categories import fixture
    result = []
    for key, value in fixture.items():
        category = Category(id=key)

        for k, v in value.items():
            setattr(category, k, v)

        category.save()
        result.append(category)
    return result

def create_default_forums():
    """This will create the 5 default groups."""
    from janitoo_manager.fixtures.forums import fixture
    result = []
    for key, value in fixture.items():
        forum = Forum(title=key)

        for k, v in value.items():
            setattr(forum, k, v)

        forum.save()
        result.append(forum)
    return result

def create_admin_user(username, password, email):
    """Creates the administrator user.
    Returns the created admin user.

    :param username: The username of the user.

    :param password: The password of the user.

    :param email: The email address of the user.
    """

    admin_group = Group.query.filter_by(admin=True).first()
    user = User()

    user.username = username
    user.password = password
    user.email = email
    user.primary_group_id = admin_group.id

    user.save()
    return user


def create_power_user(username, password, email):
    """Creates the power user.
    Returns the created power user.

    :param username: The username of the user.

    :param password: The password of the user.

    :param email: The email address of the user.
    """

    admin_group = Group.query.filter_by(admin=True).first()
    user = User()

    user.username = username
    user.password = password
    user.email = email
    user.primary_group_id = admin_group.id

    user.save()
    return user


def create_welcome_forum():
    """This will create the `welcome forum` with a welcome topic.
    Returns True if it's created successfully.
    """

    if User.query.count() < 1:
        return False

    user = User.query.filter_by(id=1).first()

    category = Category(title="My Category", position=1)
    category.save()

    forum = Forum(title="Welcome", description="Your first forum",
                  category_id=category.id)
    forum.save()

    topic = Topic(title="Welcome!")
    post = Post(content="Have fun with your new janitoo_manager Forum!")

    topic.save(user=user, forum=forum, post=post)
    return True


def create_test_data(users=5, categories=2, forums=2, topics=1, posts=1):
    """Creates 5 users, 2 categories and 2 forums in each category.
    It also creates a new topic topic in each forum with a post.
    Returns the amount of created users, categories, forums, topics and posts
    as a dict.

    :param users: The number of users.

    :param categories: The number of categories.

    :param forums: The number of forums which are created in each category.

    :param topics: The number of topics which are created in each forum.

    :param posts: The number of posts which are created in each topic.
    """
    create_default_groups()
    create_default_settings()

    data_created = {'users': 0, 'categories': 0, 'forums': 0,
                    'topics': 0, 'posts': 0}

    # create 5 users
    for u in range(1, users + 1):
        username = "test%s" % u
        email = "test%s@example.org" % u
        user = User(username=username, password="test", email=email)
        user.primary_group_id = u
        user.save()
        data_created['users'] += 1

    user1 = User.query.filter_by(id=1).first()
    user2 = User.query.filter_by(id=2).first()

    # lets send them a few private messages
    for i in range(1, 3):
        # TODO
        pass

    # create 2 categories
    for i in range(1, categories + 1):
        category_title = "Test Category %s" % i
        category = Category(title=category_title,
                            description="Test Description")
        category.save()
        data_created['categories'] += 1

        # create 2 forums in each category
        for j in range(1, forums + 1):
            if i == 2:
                j += 2

            forum_title = "Test Forum %s %s" % (j, i)
            forum = Forum(title=forum_title, description="Test Description",
                          category_id=i)
            forum.save()
            data_created['forums'] += 1

            for t in range(1, topics + 1):
                # create a topic
                topic = Topic()
                post = Post()

                topic.title = "Test Title %s" % j
                post.content = "Test Content"
                topic.save(post=post, user=user1, forum=forum)
                data_created['topics'] += 1

                for p in range(1, posts + 1):
                    # create a second post in the forum
                    post = Post()
                    post.content = "Test Post"
                    post.save(user=user2, topic=topic)
                    data_created['posts'] += 1

    return data_created


def insert_mass_data(topics=100, posts=100):
    """Creates a few topics in the first forum and each topic has
    a few posts. WARNING: This might take very long!
    Returns the count of created topics and posts.

    :param topics: The amount of topics in the forum.
    :param posts: The number of posts in each topic.
    """
    user1 = User.query.filter_by(id=1).first()
    user2 = User.query.filter_by(id=2).first()
    forum = Forum.query.filter_by(id=1).first()

    created_posts = 0
    created_topics = 0

    if not (user1 or user2 or forum):
        return False

    # create 1000 topics
    for i in range(1, topics + 1):

        # create a topic
        topic = Topic()
        post = Post()

        topic.title = "Test Title %s" % i
        post.content = "Test Content"
        topic.save(post=post, user=user1, forum=forum)
        created_topics += 1

        # create 100 posts in each topic
        for j in range(1, posts + 1):
            post = Post()
            post.content = "Test Post"
            post.save(user=user2, topic=topic)
            created_posts += 1

    return created_topics, created_posts

def create_default_modules_categories():
    """This will create the 5 default groups."""
    from janitoo_manager.fixtures.modules_categories import fixture
    result = []
    for key, value in fixture.items():
        category = ModuleCategory(id=key)

        for k, v in value.items():
            setattr(category, k, v)

        category.save()
        result.append(category)
    return result

def create_default_modules():
    """This will create the 5 default groups."""
    from janitoo_manager.fixtures.modules import fixture
    result = []
    version = "0.0.6"
    for key, value in fixture.items():
        modul = Module(uuid=key)

        for k, v in value.items():
            setattr(modul, k, v)
        modul.save()
        result.append(modul)
    return result

def populates_modules():
    """This will create the 5 default groups."""
    versions = ["0.0.6", "0.0.7", "0.0.8", "0.0.9"]
    moduls = Module.query.all()
    for version in versions:
        for modul in moduls:
            if modul.directory and modul.archive_pattern and os.path.isfile(os.path.join(modul.directory, modul.archive_pattern%version)):
                print "============ module %s" % (modul.archive_pattern%version)
                modul.import_archive(os.path.join(modul.directory, modul.archive_pattern%version))
