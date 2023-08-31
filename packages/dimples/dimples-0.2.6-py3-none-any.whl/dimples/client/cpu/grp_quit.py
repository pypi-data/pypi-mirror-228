# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Quit Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. quit the group
    2. owner and administrator cannot quit
"""

from typing import List

from dimsdk import ID
from dimsdk import ReliableMessage
from dimsdk import Content
from dimsdk import GroupCommand, QuitCommand

from .history import GroupCommandProcessor


class QuitCommandProcessor(GroupCommandProcessor):

    # Override
    def process_content(self, content: Content, r_msg: ReliableMessage) -> List[Content]:
        assert isinstance(content, QuitCommand), 'quit command error: %s' % content
        group = content.group
        # 1. check group
        owner = self.group_owner(group=group)
        members = self.group_members(group=group)
        if owner is None or len(members) == 0:
            return self._respond_receipt(text='Group empty.', msg=r_msg, group=group, extra={
                'template': 'Group empty: ${ID}',
                'replacements': {
                    'ID': str(group),
                }
            })
        # 2. check permission
        sender = r_msg.sender
        if sender == owner:
            return self._respond_receipt(text='Permission denied.', msg=r_msg, group=group, extra={
                'template': 'Owner cannot quit from group: ${ID}',
                'replacements': {
                    'ID': str(group),
                }
            })
        administrators = self.group_administrators(group=group)
        if sender in administrators:
            return self._respond_receipt(text='Permission denied.', msg=r_msg, group=group, extra={
                'template': 'Administrator cannot quit from group: ${ID}',
                'replacements': {
                    'ID': str(group),
                }
            })
        # 3. do quit
        if sender in members:
            members.remove(sender)
            if self.save_members(members=members, group=group):
                content['removed'] = [str(sender)]
        # 4. send reset command
        self.__broadcast_reset_command(group=group, members=members, sender=sender)
        # no need to response this group command
        return []

    def __broadcast_reset_command(self, group: ID, members: List[ID], sender: ID):
        """ send a reset command with newest members to the bots """
        owner = self.group_owner(group=group)
        assistants = self.group_assistants(group=group)
        administrators = self.group_administrators(group=group)
        user = self.facebook.current_user
        if user.identifier == owner or user.identifier in administrators:
            # this is the group owner (or administrator), so
            # it has permission to reset group members here.
            content = GroupCommand.reset(group=group, members=members)
            messenger = self.messenger
            if len(assistants) == 0:
                messenger.send_content(sender=user.identifier, receiver=sender, content=content, priority=1)
                return True
            for bot in assistants:
                messenger.send_content(sender=user.identifier, receiver=bot, content=content, priority=1)
                return True
