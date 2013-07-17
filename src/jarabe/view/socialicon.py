# Copyright (C) 2006-2007 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
from gi.repository import Gtk

from sugar3.graphics import style
from sugar3.graphics.icon import CanvasIcon, EventIcon

from jarabe.view.buddymenu import BuddyMenu
from jarabe.util.normalize import normalize_string

from jarabe.webservice.account import WebServicePost


_FILTERED_ALPHA = 0.33

class MockWebServicePost(WebServicePost):
    def get_title(self):
        ''' get_title returns the title of the post '''
        return "Title"

    def get_message(self):
        ''' get_message returns the message of the post '''
        return "This is a long message"

    def get_picture(self):
        ''' get_picture returns the picture attached to the post '''
        return "This is not a picture"

    def get_link(self):
        ''' get_link returns any link in the post '''
        return "http://sugarlabs.org"

post = MockWebServicePost()

class SocialIcon(CanvasIcon):
    def __init__(self, buddy, social_bubble, pixel_size=style.STANDARD_ICON_SIZE):
        CanvasIcon.__init__(self, icon_name='social-bubble',
                            pixel_size=pixel_size)

        self._social_bubble = social_bubble

        self._filtered = False
        self._buddy = buddy
        self._buddy.connect('notify::present', self.__buddy_notify_present_cb)
        self._buddy.connect('notify::color', self.__buddy_notify_color_cb)

        self.connect_after('button-release-event',
                           self.__button_release_event_cb)

        self._update_color()

    def __buddy_notify_present_cb(self, buddy, pspec):
        # Update the icon's color when the buddy comes and goes
        self._update_color()

    def __buddy_notify_color_cb(self, buddy, pspec):
        self._update_color()

    def __button_release_event_cb(self, icon, event):
        self._social_bubble.show_all()
        self.hide()
        logging.debug('SugarWebService %s' % post.get_title())

    def _update_color(self):
        # keep the icon in the palette in sync with the view
        palette = self.get_palette()
        self.props.xo_color = self._buddy.get_color()
        if self._filtered:
            self.alpha = _FILTERED_ALPHA
            if palette is not None:
                palette.props.icon.props.stroke_color = self.props.stroke_color
                palette.props.icon.props.fill_color = self.props.fill_color
        else:
            self.alpha = 1.0
            if palette is not None:
                palette.props.icon.props.xo_color = self._buddy.get_color()

    def set_filter(self, query):
        normalized_name = normalize_string(
            self._buddy.get_nick().decode('utf-8'))
        self._filtered = (normalized_name.find(query) == -1) \
            and not self._buddy.is_owner()
        self._update_color()

class SocialBubble(EventIcon):
    def __init__(self, buddy, pixel_size=style.SOCIAL_ICON_SIZE):
        EventIcon.__init__(self, icon_name='social-bubble',
                           pixel_size=pixel_size)
        # self.connect('enter-notify-event', self.__enter_notify_event_cb)
        # self.connect('leave-notify-event', self.__leave_notify_event_cb)
        self.set_visible_window(True)
        self.set_above_child(False)

        self._filtered = False
        self._buddy = buddy
        label = Gtk.Label('Sample Text')
        self.add(label)

        self._buddy.connect('notify::present', self.__buddy_notify_present_cb)
        self._buddy.connect('notify::color', self.__buddy_notify_color_cb)


        self._update_color()

    def __buddy_notify_present_cb(self, buddy, pspec):
        # Update the icon's color when the buddy comes and goes
        self._update_color()

    def __buddy_notify_color_cb(self, buddy, pspec):
        self._update_color()

    def _update_color(self):
        # keep the icon in the palette in sync with the view
        palette = self.get_palette()
        self.props.xo_color = self._buddy.get_color()
        if self._filtered:
            self.alpha = _FILTERED_ALPHA
            if palette is not None:
                palette.props.icon.props.stroke_color = self.props.stroke_color
                palette.props.icon.props.fill_color = self.props.fill_color
        else:
            self.alpha = 1.0
            if palette is not None:
                palette.props.icon.props.xo_color = self._buddy.get_color()

    def set_filter(self, query):
        normalized_name = normalize_string(
            self._buddy.get_nick().decode('utf-8'))
        self._filtered = (normalized_name.find(query) == -1) \
            and not self._buddy.is_owner()
        self._update_color()
