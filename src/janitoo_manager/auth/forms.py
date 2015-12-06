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
logger = logging.getLogger(__name__)

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField, HiddenField,
                     SubmitField, SelectField)
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo,
                                regexp, ValidationError)
from flask_babelex import lazy_gettext as _
from janitoo_manager.user.models import UserMan

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=_("You can only use letters, numbers or dashes."))


class LoginForm(Form):
    login = StringField(_("Username or E-Mail Address"), validators=[
        DataRequired(message=_("A Username or E-Mail Address is required."))]
    )

    password = PasswordField(_("Password"), validators=[
        DataRequired(message=_("A Password is required."))])

    remember_me = BooleanField(_("Remember Me"), default=False)

    submit = SubmitField(_("Login"))


class RegisterForm(Form):
    username = StringField(_("Username"), validators=[
        DataRequired(message=_("A Username is required.")),
        is_username])

    email = StringField(_("E-Mail Address"), validators=[
        DataRequired(message=_("A E-Mail Address is required.")),
        Email(message=_("Invalid E-Mail Address."))])

    password = PasswordField(_('Password'), validators=[
        InputRequired(),
        EqualTo('confirm_password', message=_('Passwords must match.'))])

    confirm_password = PasswordField(_('Confirm Password'))


    language = SelectField(_('Language'))

    accept_tos = BooleanField(_("I accept the Terms of Service"), default=True)

    submit = SubmitField(_("Register"))

    def validate_username(self, field):
        user = UserMan.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(_("This Username is already taken."))

    def validate_email(self, field):
        email = UserMan.query.filter_by(email=field.data).first()
        if email:
            raise ValidationError(_("This E-Mail Address is already taken."))

    def save(self):
        user = UserMan(username=self.username.data,
                    email=self.email.data,
                    password=self.password.data,
                    date_joined=datetime.utcnow(),
                    primary_group_id=4,
                    language=self.language.data)
        return user.save()


class RegisterRecaptchaForm(RegisterForm):
    recaptcha = RecaptchaField(_("Captcha"))


class ReauthForm(Form):
    password = PasswordField(_('Password'), valdidators=[
        DataRequired(message=_("A Password is required."))])

    submit = SubmitField(_("Refresh Login"))


class ForgotPasswordForm(Form):
    email = StringField(_('E-Mail Address'), validators=[
        DataRequired(message=_("A E-Mail Address is reguired.")),
        Email()])

    submit = SubmitField(_("Request Password"))


class ResetPasswordForm(Form):
    token = HiddenField('Token')

    email = StringField(_('E-Mail Address'), validators=[
        DataRequired(message=_("A E-Mail Address is required.")),
        Email()])

    password = PasswordField(_('Password'), validators=[
        InputRequired(),
        EqualTo('confirm_password', message=_('Passwords must match.'))])

    confirm_password = PasswordField(_('Confirm Password'))

    submit = SubmitField(_("Reset Password"))

    def validate_email(self, field):
        email = UserMan.query.filter_by(email=field.data).first()
        if not email:
            raise ValidationError(_("Wrong E-Mail Address."))
