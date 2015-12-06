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

import simplejson as json
from datetime import datetime
from wtforms.widgets.core import Select, HTMLString, html_params


class SelectBirthdayWidget(object):
    """Renders a DateTime field with 3 selects.
    For more information see: http://stackoverflow.com/a/14664504
    """
    FORMAT_CHOICES = {
        '%d': [(x, str(x)) for x in range(1, 32)],
        '%m': [(x, str(x)) for x in range(1, 13)]
    }

    FORMAT_CLASSES = {
        '%d': 'select_date_day',
        '%m': 'select_date_month',
        '%Y': 'select_date_year'
    }

    def __init__(self, years=range(1930, datetime.utcnow().year + 1)):
        """Initialzes the widget.

        :param years: The min year which should be chooseable.
                      Defatuls to ``1930``.
        """
        super(SelectBirthdayWidget, self).__init__()
        self.FORMAT_CHOICES['%Y'] = [(x, str(x)) for x in years]

    def __call__(self, field, **kwargs):
        field_id = kwargs.pop('id', field.id)
        html = []
        allowed_format = ['%d', '%m', '%Y']
        surrounded_div = kwargs.pop('surrounded_div', None)
        css_class = kwargs.get('class', None)

        for date_format in field.format.split():
            if date_format in allowed_format:
                choices = self.FORMAT_CHOICES[date_format]
                id_suffix = date_format.replace('%', '-')
                id_current = field_id + id_suffix

                if css_class is not None:  # pragma: no cover
                    select_class = "{} {}".format(
                        css_class, self.FORMAT_CLASSES[date_format]
                    )
                else:
                    select_class = self.FORMAT_CLASSES[date_format]

                kwargs['class'] = select_class

                try:
                    del kwargs['placeholder']
                except KeyError:
                    pass

                if surrounded_div is not None:
                    html.append('<div class="%s">' % surrounded_div)

                html.append('<select %s>' % html_params(name=field.name,
                                                        id=id_current,
                                                        **kwargs))

                if field.data:
                    current_value = int(field.data.strftime(date_format))
                else:
                    current_value = None

                for value, label in choices:
                    selected = (value == current_value)

                    # Defaults to blank
                    if value == 1 or value == 1930:
                        html.append(Select.render_option("None", " ", selected))

                    html.append(Select.render_option(value, label, selected))

                html.append('</select>')

                if surrounded_div is not None:
                    html.append("</div>")

            html.append(' ')

        return HTMLString(''.join(html))


class MultiSelect(object):
    """
    Renders a megalist-multiselect widget.


    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected)`.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        src_list, dst_list = [], []

        for val, label, selected in field.iter_choices():
            if selected:
                dst_list.append({'label':label, 'listValue':val})
            else:
                src_list.append({'label':label, 'listValue':val})
        kwargs.update(
            {
                'data-provider-src':json.dumps(src_list),
                'data-provider-dst':json.dumps(dst_list)
            }
        )
        html = ['<div %s>' % html_params(name=field.name, **kwargs)]
        html.append('</div>')
        return HTMLString(''.join(html))
