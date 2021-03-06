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

from flask_wtf import Form
from wtforms import (StringField, TextAreaField, PasswordField, IntegerField,
                     BooleanField, SelectField, SubmitField,
             HiddenField)
from wtforms.validators import (DataRequired, Optional, Email, regexp, Length,
                                URL, ValidationError)
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from sqlalchemy.orm.session import make_transient, make_transient_to_detached
from flask_babelplus import lazy_gettext as _

from janitoo_manager.utils.fields import BirthdayField
from janitoo_manager.utils.widgets import SelectBirthdayWidget, MultiSelect
from janitoo_manager.extensions import db
import janitoo_db.models as jnt_models

USERNAME_RE = r'^[\w.+-]+$'
is_username = regexp(USERNAME_RE,
                     message=_("You can only use letters, numbers or dashes."))


def selectable_forums():
    return jnt_models.Forum.query.order_by(jnt_models.Forum.position)


def selectable_categories():
    return jnt_models.Category.query.order_by(jnt_models.Category.position)


def selectable_groups():
    return jnt_models.Group.query.order_by(jnt_models.Group.id.asc()).all()


def select_primary_group():
    return jnt_models.Group.query.filter(jnt_models.Group.guest != True).order_by(jnt_models.Group.id)


class UserForm(Form):
    username = StringField(_("Username"), validators=[
        DataRequired(message=_("A Username is required.")),
        is_username])

    email = StringField(_("E-Mail Address"), validators=[
        DataRequired(message=_("A E-Mail Address is required.")),
        Email(message=_("Invalid E-Mail Address."))])

    password = PasswordField("Password", validators=[
        Optional()])

    birthday = BirthdayField(_("Birthday"), format="%d %m %Y",
                             widget=SelectBirthdayWidget(),
                             validators=[Optional()])

    gender = SelectField(_("Gender"), default="None", choices=[
        ("None", ""),
        ("Male", _("Male")),
        ("Female", _("Female"))])

    location = StringField(_("Location"), validators=[
        Optional()])

    website = StringField(_("Website"), validators=[
        Optional(), URL()])

    avatar = StringField(_("Avatar"), validators=[
        Optional(), URL()])

    signature = TextAreaField(_("Forum Signature"), validators=[
        Optional(), Length(min=0, max=250)])

    notes = TextAreaField(_("Notes"), validators=[
        Optional(), Length(min=0, max=5000)])

    primary_group = QuerySelectField(
        _("Primary Group"),
        query_factory=select_primary_group,
        get_label="name")

    secondary_groups = QuerySelectMultipleField(
        _("Secondary Groups"),
        # TODO: Template rendering errors "NoneType is not callable"
        #       without this, figure out why.
        query_factory=select_primary_group,
        get_label="name")

    submit = SubmitField(_("Save"))

    def validate_username(self, field):
        if hasattr(self, "user"):
            user = jnt_models.User.query.filter(
                db.and_(
                    jnt_models.User.username.like(field.data),
                    db.not_(User.id == self.user.id)
                )
            ).first()
        else:
            user = jnt_models.User.query.filter(jnt_models.User.username.like(field.data)).first()

        if user:
            raise ValidationError(_("This Username is already taken."))

    def validate_email(self, field):
        if hasattr(self, "user"):
            user = jnt_models.User.query.filter(
                db.and_(
                    jnt_models.User.email.like(field.data),
                    db.not_(User.id == self.user.id)
                )
            ).first()
        else:
            user = jnt_models.User.query.filter(jnt_models.User.email.like(field.data)).first()

        if user:
            raise ValidationError(_("This E-Mail Address is already taken."))

    def save(self):
        data = self.data
        data.pop('submit', None)
        user = jnt_models.User(**data)
        return user.save()


class AddUserForm(UserForm):
    pass


class EditUserForm(UserForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        kwargs['obj'] = self.user
        UserForm.__init__(self, *args, **kwargs)


class GroupForm(Form):
    name = StringField(_("Group Name"), validators=[
        DataRequired(message=_("A Group name is required."))])

    description = TextAreaField(_("Description"), validators=[
        Optional()])

    admin = BooleanField(
        _("Is Admin Group?"),
        description=_("With this option the group has access to "
                      "the admin panel.")
    )
    super_mod = BooleanField(
        _("Is Super Moderator Group?"),
        description=_("Check this if the users in this group are allowed to "
                      "moderate every forum.")
    )
    mod = BooleanField(
        _("Is Moderator Group?"),
        description=_("Check this if the users in this group are allowed to "
                      "moderate specified forums.")
    )
    banned = BooleanField(
        _("Is Banned Group?"),
        description=_("Only one Banned group is allowed.")
    )
    guest = BooleanField(
        _("Is Guest Group?"),
        description=_("Only one Guest group is allowed.")
    )
    editpost = BooleanField(
        _("Can edit posts"),
        description=_("Check this if the users in this group can edit posts.")
    )
    deletepost = BooleanField(
        _("Can delete posts"),
        description=_("Check this is the users in this group can delete posts.")
    )
    deletetopic = BooleanField(
        _("Can delete topics"),
        description=_("Check this is the users in this group can delete "
                      "topics.")
    )
    posttopic = BooleanField(
        _("Can create topics"),
        description=_("Check this is the users in this group can create "
                      "topics.")
    )
    postreply = BooleanField(
        _("Can post replies"),
        description=_("Check this is the users in this group can post replies.")
    )

    mod_edituser = BooleanField(
        _("Moderators can edit user profiles"),
        description=_("Allow moderators to edit a another users profile "
                      "including password and email changes.")
    )

    mod_banuser = BooleanField(
        _("Moderators can ban users"),
        description=_("Allow moderators to ban other users.")
    )

    submit = SubmitField(_("Save"))

    def validate_name(self, field):
        if hasattr(self, "group"):
            group = jnt_models.Group.query.filter(
                db.and_(
                    jnt_models.Group.name.like(field.data),
                    db.not_(jnt_models.Group.id == self.group.id)
                )
            ).first()
        else:
            group = jnt_models.Group.query.filter(jnt_models.Group.name.like(field.data)).first()

        if group:
            raise ValidationError(_("This Group name is already taken."))

    def validate_banned(self, field):
        if hasattr(self, "group"):
            group = jnt_models.Group.query.filter(
                db.and_(
                    jnt_models.Group.banned,
                    db.not_(jnt_models.Group.id == self.group.id)
                )
            ).count()
        else:
            group = jnt_models.Group.query.filter_by(banned=True).count()

        if field.data and group > 0:
            raise ValidationError(_("There is already a Banned group."))

    def validate_guest(self, field):
        if hasattr(self, "group"):
            group = jnt_models.Group.query.filter(
                db.and_(
                    jnt_models.Group.guest,
                    db.not_(jnt_models.Group.id == self.group.id)
                )
            ).count()
        else:
            group = jnt_models.Group.query.filter_by(guest=True).count()

        if field.data and group > 0:
            raise ValidationError(_("There is already a Guest group."))

    def save(self):
        data = self.data
        data.pop('submit', None)
        group = jnt_models.Group(**data)
        return group.save()


class EditGroupForm(GroupForm):
    def __init__(self, group, *args, **kwargs):
        self.group = group
        kwargs['obj'] = self.group
        GroupForm.__init__(self, *args, **kwargs)


class AddGroupForm(GroupForm):
    pass


class ForumForm(Form):
    title = StringField(
        _("Forum Title"),
        validators=[DataRequired(message=_("A Forum Title is required."))]
    )

    description = TextAreaField(
        _("Description"),
        validators=[Optional()],
        description=_("You can format your description with BBCode.")
    )

    position = IntegerField(
        _("Position"),
        default=1,
        validators=[DataRequired(message=_("The Forum Position is required."))]
    )

    category = QuerySelectField(
        _("Category"),
        query_factory=selectable_categories,
        allow_blank=False,
        get_label="title",
        description=_("The category that contains this forum.")
    )

    external = StringField(
        _("External Link"),
        validators=[Optional(), URL()],
        description=_("A link to a website i.e. 'http://janitoo_manager.org'.")
    )

    moderators = StringField(
        _("Moderators"),
        description=_("Comma seperated usernames. Leave it blank if you do not "
                      "want to set any moderators.")
    )

    show_moderators = BooleanField(
        _("Show Moderators"),
        description=_("Do you want show the moderators on the index page?")
    )

    locked = BooleanField(
        _("Locked?"),
        description=_("Disable new posts and topics in this forum.")
    )

    groups = QuerySelectMultipleField(
        _("Group Access to Forum"),
        query_factory=selectable_groups,
        get_label="name",
        description=_("Select user groups that can access this forum.")
    )

    submit = SubmitField(_("Save"))

    def validate_external(self, field):
        if hasattr(self, "forum"):
            if self.forum.topics:
                raise ValidationError(_("You cannot convert a forum that "
                                        "contain topics in a external link."))

    def validate_show_moderators(self, field):
        if field.data and not self.moderators.data:
            raise ValidationError(_("You also need to specify some "
                                    "moderators."))

    def validate_moderators(self, field):
        approved_moderators = list()

        if field.data:
            # convert the CSV string in a list
            moderators = field.data.split(",")
            # remove leading and ending spaces
            moderators = [mod.strip() for mod in moderators]
            for moderator in moderators:
                # Check if the usernames exist
                user = jnt_models.User.query.filter_by(username=moderator).first()

                # Check if the user has the permissions to moderate a forum
                if user:
                    if not (user.get_permissions()["mod"] or
                            user.get_permissions()["admin"] or
                            user.get_permissions()["super_mod"]):
                        raise ValidationError(
                            _("%(user)s is not in a moderators group.",
                              user=user.username)
                        )
                    else:
                        approved_moderators.append(user)
                else:
                    raise ValidationError(_("User %(moderator)s not found.",
                                            moderator=moderator))
            field.data = approved_moderators

        else:
            field.data = approved_moderators

    def save(self):
        data = self.data
        # remove the button
        data.pop('submit', None)
        forum = jnt_models.Forum(**data)
        return forum.save()


class EditForumForm(ForumForm):

    id = HiddenField()

    def __init__(self, forum, *args, **kwargs):
        self.forum = forum
        kwargs['obj'] = self.forum
        ForumForm.__init__(self, *args, **kwargs)

    def save(self):
        data = self.data
        # remove the button
        data.pop('submit', None)
        forum = jnt_models.Forum(**data)
        # flush SQLA info from created instance so that it can be merged
        make_transient(forum)
        make_transient_to_detached(forum)

        return forum.save()


class AddForumForm(ForumForm):
    pass


class CategoryForm(Form):
    title = StringField(_("Category Title"), validators=[
        DataRequired(message=_("A Category Title is required."))])

    description = TextAreaField(
        _("Description"),
        validators=[Optional()],
        description=_("You can format your description with BBCode.")
    )

    position = IntegerField(
        _("Position"),
        default=1,
        validators=[DataRequired(message=_("The Category Position is "
                                           "required."))]
    )

    submit = SubmitField(_("Save"))

    def save(self):
        data = self.data
        data.pop('submit', None)
        category = jnt_models.Category(**data)
        return jnt_models.category.save()
