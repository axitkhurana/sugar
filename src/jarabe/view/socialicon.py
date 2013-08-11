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
from sugar3.graphics.icon import Icon, CanvasIcon, EventIcon

from jarabe.view.buddymenu import BuddyMenu
from jarabe.util.normalize import normalize_string

_FILTERED_ALPHA = 0.33


class SmallCloudIcon(CanvasIcon):
    def __init__(self, buddy, social_cloud, pixel_size=style.STANDARD_ICON_SIZE):
        CanvasIcon.__init__(self, icon_name='social-bubble',
                            pixel_size=pixel_size)

        self._social_cloud = social_cloud

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
        self._social_cloud.show_all()
        self.hide()

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


class LargeCloudIcon(EventIcon):
    def __init__(self, buddy, pixel_size=style.SOCIAL_ICON_SIZE):
        EventIcon.__init__(self, icon_name='social-bubble-large',
                           pixel_size=pixel_size)
        # self.connect('enter-notify-event', self.__enter_notify_event_cb)
        # self.connect('leave-notify-event', self.__leave_notify_event_cb)
        self._filtered = False
        self._buddy = buddy

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


class CloudContent(Gtk.VBox):
    def __init__(self, text, service_icon):
        Gtk.VBox.__init__(self)
        self.set_homogeneous(False)
        label = Gtk.Label(text)
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.CENTER)

        self._text = Gtk.HBox()
        self._text.pack_start(label, False, False, 20)
        self._icon = Icon(pixel_size=style.SOCIAL_POST_ICON_SIZE,
                          icon_name=service_icon,
                          stroke_color=style.COLOR_BLACK.get_svg(),
                          fill_color=style.COLOR_WHITE.get_svg())
        self.pack_start(self._icon, False, True, 60)
        self.pack_end(self._text, False, True, 80)


class SocialCloud(Gtk.Overlay):
    def __init__(self, buddy, text, service_icon_name):
        Gtk.Overlay.__init__(self)
        self.icon = LargeCloudIcon(buddy)
        self.content = CloudContent(text, service_icon_name)

        self.add(self.icon)
        self.add_overlay(self.content)
