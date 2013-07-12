# Copyright (c) 2013 Walter Bender, Raul Gutierrez Segales
# Copyright (c) 2013 SugarLabs
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from gi.repository import GObject


class Account():
    ''' Account is a prototype class for online accounts. It provides
    stubs for public methods that are used by online services.
    '''

    STATE_NONE = 0
    STATE_VALID = 1
    STATE_EXPIRED = 2

    def get_description(self):
        ''' get_description returns a brief description of the online
        service. The description is used in palette menuitems and on
        the webservices control panel.

        :returns: online-account name
        :rtype: string
        '''
        raise NotImplementedError

    def get_token_state(self):
        ''' get_token_state returns an enum to describe the state of
        the online service:
        State.NONE means there is no token, e.g., the service is not
            configured.
        State.VALID means there is a valid token, e.g., the service is
            available for use.
        State.EXPIRED means the token is no longer valid.

        :returns: token state
        :rtype: enum
        '''
        raise NotImplementedError

    def get_shared_journal_entry(self):
        ''' get_shared_journal_entry returns a class used to
        intermediate between the online service and the Sugar UI
        elements.

        :returns: SharedJournalEntry()
        :rtype: SharedJournalEntry
        '''
        return NotImplemented

    def get_public_id(self):
        ''' get_public_id returns a string which identifies the user uniquely
        on the online service

        :returns: unique public id
        :rtype: string
        '''
        raise NotImplementedError

    def get_latest_post(self):
        ''' get_latest_post returns a class that has the latest post on the
        online service

        :returns: WebServicePost()
        :rtype: WebServicePost
        '''
        raise NotImplementedError

class SharedJournalEntry():
    ''' SharedJournalEntry is a class used to intermediate between the
    online service and the Sugar UI elements (MenuItems used in the
    Journal UI) for online accounts. It provides stubs for public
    methods that are used by online services.

    The comments-changed signal is emitted by the online service if
    changes to the 'comments' metadata have been made.

    :emits: metadata['comments']
    :type: string
    '''

    __gsignals__ = {
        'comments-changed': (GObject.SignalFlags.RUN_FIRST, None, ([str]))
    }

    def get_share_menu(self, metadata):
        ''' get_share_menu returns a menu item used on the Copy To
        palette in the Journal and on the Journal detail-view toolbar.

        :param: journal_entry_metadata
        :type: dict
        :returns: MenuItem
        :rtype: MenuItem
        '''
        raise NotImplementedError

    def get_refresh_menu(self):
        ''' get_refresh_menu returns a menu item used on the Journal
        detail-view toolbar.

        :returns: MenuItem
        :rtype: MenuItem
        '''
        raise NotImplementedError

    def set_metadata(self, metadata):
        ''' The online account uses this method to set metadata in the
        Sugar journal and provide a means of updating menuitem status,
        e.g., enabling the refresh menu after a successful transfer.

        :param: journal_entry_metadata
        :type: dict
        '''
        raise NotImplementedError

class WebServicePost():
    ''' WebServicePost is a class used as a general representation of a
    post from any external web service. It provides stubs for public methods
    for accessing post data that are used by the social sugar widget.

    It holds the latest public post on the service. The post-changed signal is
    emitted by the online service if newer post has been posted on the service.
    '''

    __gsignals__ = {
        'post-changed': (GObject.SignalFlags.RUN_FIRST, None, ([]))
    }

    def get_title(self):
        ''' get_title returns the title of the post '''
        raise NotImplementedError

    def get_message(self):
        ''' get_message returns the message of the post '''
        raise NotImplementedError

    def get_picture(self):
        ''' get_picture returns the picture attached to the post '''
        raise NotImplementedError

    def get_link(self):
        ''' get_link returns any link in the post '''
        raise NotImplementedError
