# -*- coding: utf-8 -*-
"""
    janitoo_manager.fixtures.categories
    ~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our groups.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime, timedelta
from collections import OrderedDict


fixture = OrderedDict((
    (u"janitoo", {
        u'title': u"Core",
        u'description': u"Janitoo's core",
        u'archive_pattern': u"janitoo-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo/dists",
        u'category_id': 1,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_admin", {
        u'title': u"Admin",
        u'description': u"Web admin",
        u'archive_pattern': u"janitoo_admin-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_admin/dists",
        u'category_id': 1,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_hostsensor", {
        u'title': u"Hostsensor",
        u'archive_pattern': u"janitoo_hostsensor-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_hostsensor/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_hostsensor_lmsensor", {
        u'title': u"LM-sensors extension fot Hostsensor",
        u'archive_pattern': u"janitoo_hostsensor_lmsensor-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_hostsensor_lmsensor/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_hostsensor_psutil", {
        u'title': u"PSUtil extension for Hostsensor",
        u'archive_pattern': u"janitoo_hostsensor_psutil-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_hostsensor_psutil/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_hostsensor_raspberry", {
        u'title': u"Raspberry Pi extension for Hostsensor",
        u'archive_pattern': u"janitoo_hostsensor_raspberry-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_hostsensor_raspberry/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_datalog_rrd", {
        u'title': u"Datalog using Rrd",
        u'archive_pattern': u"janitoo_datalog_rrd-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_datalog_rrd/dists",
        u'category_id': 1,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_roomba", {
        u'title': u"Roomba",
        u'archive_pattern': u"janitoo_roomba-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_roomba/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_audivideo", {
        u'title': u"AudioVideo",
        u'archive_pattern': u"janitoo_audiovideo-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_audiovideo/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_nut", {
        u'title': u"Nut",
        u'archive_pattern': u"janitoo_nut-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_nut/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_pi", {
        u'title': u"Raspberry pi extensions",
        u'archive_pattern': u"janitoo_pi-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_pi/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_dhcp", {
        u'title': u"Dynamic Home Configuration Protocol server",
        u'archive_pattern': u"janitoo_dhcp-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_dhcp/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_events", {
        u'title': u"Events server",
        u'archive_pattern': u"janitoo_events-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_events/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_events_earth", {
        u'title': u"Events based on earth events (dawn, dusk, ...)",
        u'archive_pattern': u"janitoo_events_earth-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_events_earth/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_update", {
        u'title': u"Updater for janitoo",
        u'archive_pattern': u"janitoo_update-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_update/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_update_ubuntu", {
        u'title': u"Updater for ubuntu",
        u'archive_pattern': u"janitoo_update_ubuntu-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_update_ubuntu/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_update_debian", {
        u'title': u"Updater for debian",
        u'archive_pattern': u"janitoo_update_debian-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_update_debian/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_update_raspberry", {
        u'title': u"Updater for raspberry",
        u'archive_pattern': u"janitoo_update_raspberry-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_update_raspberry/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_admin_proxy", {
        u'title': u"Proxy to collect all http nodes servers",
        u'archive_pattern': u"janitoo_admin_proxy-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_admin_proxy/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"janitoo_admin_widget", {
        u'title': u"Example widget for admin",
        u'archive_pattern': u"janitoo_admin_widget-%s.tar.bz2",
        u'directory': u"/opt/janitoo/src/janitoo_admin_widget/dists",
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
    (u"python_openzwave", {
        u'title': u"Python OpenZwave",
        u'github': u"OpenZWave/python-openzwave",
        u'directory': '/opt/janitoo/src/janistore/uploads/python-openzwave',
        u'category_id': 3,
        u'date_published': datetime.utcnow(),
        u'developper_id': 2,
    }),
))
