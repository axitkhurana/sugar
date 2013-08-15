# Copyright (C) 2006-2007 Red Hat, Inc.
# Copyright (C) 2010 Collabora Ltd. <http://www.collabora.co.uk/>
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

import itertools
from gi.repository import Gtk, GObject

from sugar3.graphics import style
from sugar3.graphics.icon import CanvasIcon

from jarabe.view.buddyicon import BuddyIcon
from jarabe.view.socialicon import (SmallCloudIcon, LargeCloudIcon,
                                    CloudContent, SocialCloud)
from jarabe.model import bundleregistry
from jarabe.webservice.accountsmanager import get_all_accounts, get_account

class FriendView(Gtk.VBox):
    def __init__(self, buddy, **kwargs):
        Gtk.VBox.__init__(self)

        # round icon sizes to an even number so that it can be accurately
        # centered in a larger bounding box also of even dimensions
        size = style.LARGE_ICON_SIZE & ~1

        self._buddy = buddy
        self._buddy_icon = BuddyIcon(buddy)

        self._account_names = [account.get_description() for account in
                               get_all_accounts()]

        # cycle infinitely
        self._account_iter = itertools.cycle(self._account_names)

        self._buddy_icon.props.pixel_size = size

        self.pack_end(self._buddy_icon, False, True, 0)

        if self._buddy.get_social_ids():
            self._social_cloud_init()
            self._social_cloud.connect('show', self.__social_cloud_show_cb)

        self._buddy_icon.show()

        self._activity_icon = CanvasIcon(pixel_size=size)
        self._update_activity()

        self._buddy.connect('notify::current-activity',
                            self.__buddy_notify_current_activity_cb)
        self._buddy.connect('notify::present', self.__buddy_notify_present_cb)
        self._buddy.connect('notify::color', self.__buddy_notify_color_cb)
        self._buddy.connect('notify::social-ids',
                            self.__buddy_notify_social_ids_cb)


    def _social_cloud_init(self):
        if self._account_names:
            friend_social_ids = self._buddy.get_social_ids()

            account = self._account_names[0]
            self._account_iter.next() # start from next account

            if account in friend_social_ids:
                text, icon = self._social_cloud_content(account,
                                    friend_social_ids[account])
                self._social_cloud = SocialCloud(self._buddy, text, icon)
                self._small_cloud_icon = SmallCloudIcon(self._buddy,
                                                        self._social_cloud)
                self.pack_start(self._social_cloud, False, True, 0)
                self.pack_start(self._small_cloud_icon, False, True, 0)
                self._small_cloud_icon.show()

    def _social_cloud_content(self, account_name, friend_social_id):
        my_account = get_account(account_name)
        post = my_account.get_latest_post(friend_social_id)
        content = post.get_message()
        service_icon = post.get_picture()
        return content, service_icon

    def _next_social_post(self, social_cloud):
        if not social_cloud.props.visible:
            return False

        account_name = self._account_iter.next()
        friend_social_ids = self._buddy.get_social_ids()

        if account_name in friend_social_ids:
            text, icon = self._social_cloud_content(account_name,
                            friend_social_ids[account_name])
            social_cloud.set_text(text)
            social_cloud.set_service_icon(service_icon)

    def _get_new_icon_name(self, ps_activity):
        registry = bundleregistry.get_registry()
        activity_info = registry.get_bundle(ps_activity.props.type)
        if activity_info:
            return activity_info.get_icon()
        return None

    def _remove_activity_icon(self):
        if self._activity_icon.get_visible():
            self._activity_icon.hide()
            self.remove(self._activity_icon)

    def __buddy_notify_current_activity_cb(self, buddy, pspec):
        self._update_activity()

    def _update_activity(self):
        if not self._buddy.props.present or \
           not self._buddy.props.current_activity:
            self._remove_activity_icon()
            return

        # FIXME: use some sort of "unknown activity" icon rather
        # than hiding the icon?
        name = self._get_new_icon_name(self._buddy.current_activity)
        if name:
            self._activity_icon.props.file_name = name
            self._activity_icon.props.xo_color = self._buddy.props.color
            if not self._activity_icon.get_visible():
                self.add(self._activity_icon)
                self._activity_icon.show()
        else:
            self._remove_activity_icon()

    def __buddy_notify_present_cb(self, buddy, pspec):
        self._update_activity()

    def __buddy_notify_color_cb(self, buddy, pspec):
        # TODO: shouldn't this change self._buddy_icon instead?
        self._activity_icon.props.xo_color = buddy.props.color

    def __buddy_notify_social_ids_cb(self, buddy, pspec):
        self._social_cloud_init()
        self._social_cloud.connect('show', self.__social_cloud_show_cb)

    def __social_cloud_show_cb(self, social_cloud, pspec):
        GObject.timeout_add(5000, self._next_social_post, social_cloud)
