#!/usr/bin/python
# -*- coding: utf-8 -*-

"""UWSGI scripts

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

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014-2015-2016 Sébastien GALLET aka bibi21000"
#~ try:
    #~ from gevent import monkey
    #~ monkey.patch_all()
#~ except ImportError:
    #~ pass
from janitoo_manager.app import create_app
from janitoo_manager.configs.production import ProductionConfig
from janitoo_manager.extensions import socketio

application = create_app(config=ProductionConfig('/opt/janitoo/etc/janitoo_manager.conf'))

#~ import jinja2
#~ from janitoo_web.app import create_app, run_app
#~ from janitoo_admin.app import app as application, socketio
#~ from janitoo.runner import jnt_parse_args

#args = jnt_parse_args()
#options = vars(args)
#~ options = {}
#~ options["conf_file"] = "/var/www/janitoo_admin.conf"
#~ options["home_dir"] = "/var/www/"
#~ application, socketio = create_app(config_object='janitoo_web.config.RunConfig', options=options)
    #app.run(debug=True)
    #socketio.run(app)
    #print app
#application.jinja_loader = jinja2.FileSystemLoader('/home/sebastien/devel/janitoo/src-admin/scripts/admin/default')
if __name__ == '__main__':
    #~ run_app(application, socketio)
    socketio.run(app)
