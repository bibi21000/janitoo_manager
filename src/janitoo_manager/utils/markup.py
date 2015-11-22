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

import os
import re

from flask import url_for

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


_re_emoji = re.compile(r':([a-z0-9\+\-_]+):', re.I)
_re_user = re.compile(r'@(\w+)', re.I)

# base directory of janitoo_manager - used to collect the emojis
_basedir = os.path.join(os.path.abspath(os.path.dirname(
                        os.path.dirname(__file__))))


def collect_emojis():
    """Returns a dictionary containing all emojis with their
    name and filename. If the folder doesn't exist it returns a empty
    dictionary.
    """
    emojis = dict()
    full_path = os.path.join(_basedir, "static", "emoji")
    # return an empty dictionary if the path doesn't exist
    if not os.path.exists(full_path):
        return emojis

    for emoji in os.listdir(full_path):
        name, ending = emoji.split(".")
        if ending in ["png", "gif", "jpg", "jpeg"]:
            emojis[name] = emoji

    return emojis

EMOJIS = collect_emojis()


class JanitooManagerRenderer(mistune.Renderer):
    """Markdown with some syntetic sugar such as @user gets linked to the
    user's profile and emoji support.
    """
    def __init__(self, **kwargs):
        super(JanitooManagerRenderer, self).__init__(**kwargs)

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>`` with emoji support."""

        def emojify(match):
            value = match.group(1)

            if value in EMOJIS:
                filename = url_for(
                    "static",
                    filename="emoji/{}".format(EMOJIS[value])
                )

                emoji = "<img class='{css}' alt='{alt}' src='{src}' />".format(
                    css="emoji", alt=value,
                    src=filename
                )
                return emoji
            return match.group(0)

        def userify(match):
            value = match.group(1)
            user = "<a href='{url}'>@{user}</a>".format(
                url=url_for("user.profile", username=value, _external=False),
                user=value
            )
            return user

        text = _re_emoji.sub(emojify, text)
        text = _re_user.sub(userify, text)

        return '<p>%s</p>\n' % text.strip(' ')

    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = JanitooManagerRenderer()
markdown = mistune.Markdown(renderer=renderer)
