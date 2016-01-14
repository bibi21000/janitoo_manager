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

from flask import Blueprint, flash, request
from flask_login import login_required, current_user
from flask_themes2 import get_themes_list
from flask_babelex import gettext as _

from janitoo_manager.extensions import babel
from janitoo_manager.utils.helpers import render_template
from janitoo_manager.user.models import UserMan
from janitoo_manager.user.forms import (ChangePasswordForm, ChangeEmailForm,
                                ChangeUserDetailsForm, GeneralSettingsForm)


user = Blueprint("user", __name__)


@user.route("/<username>")
def profile(username):
    user = UserMan.query.filter_by(username=username).first_or_404()

    return render_template("user/profile.html", user=user)


@user.route("/settings/general", methods=["POST", "GET"])
@login_required
def settings():
    form = GeneralSettingsForm()

    form.theme.choices = [(theme.identifier, theme.name)
                          for theme in get_themes_list()]

    form.language.choices = [(locale.language, locale.display_name)
                             for locale in babel.list_translations()]

    if form.validate_on_submit():
        current_user.theme = form.theme.data
        current_user.language = form.language.data
        current_user.save()

        flash(_("Settings updated."), "success")
    else:
        form.theme.data = current_user.theme
        form.language.data = current_user.language

    return render_template("user/general_settings.html", form=form)


@user.route("/settings/password", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        current_user.save()

        flash(_("Password updated."), "success")
    return render_template("user/change_password.html", form=form)


@user.route("/settings/email", methods=["POST", "GET"])
@login_required
def change_email():
    form = ChangeEmailForm(current_user)
    if form.validate_on_submit():
        current_user.email = form.new_email.data
        current_user.save()

        flash(_("E-Mail Address updated."), "success")
    return render_template("user/change_email.html", form=form)


@user.route("/settings/user-details", methods=["POST", "GET"])
@login_required
def change_user_details():
    form = ChangeUserDetailsForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash(_("Details updated."), "success")

    return render_template("user/change_user_details.html", form=form)
