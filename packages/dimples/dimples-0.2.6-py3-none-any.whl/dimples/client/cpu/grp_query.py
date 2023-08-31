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
    Query Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. query for group members-list
    2. any existed member or assistant can query group members-list
"""

from typing import List

from dimsdk import ReliableMessage
from dimsdk import Content
from dimsdk import QueryCommand

from .history import GroupCommandProcessor


class QueryCommandProcessor(GroupCommandProcessor):

    # Override
    def process_content(self, content: Content, r_msg: ReliableMessage) -> List[Content]:
        assert isinstance(content, QueryCommand), 'query command error: %s' % content
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
        assistants = self.group_assistants(group=group)
        # 2. check permission
        sender = r_msg.sender
        if sender not in members and sender not in assistants:
            return self._respond_receipt(text='Permission denied.', msg=r_msg, group=group, extra={
                'template': 'Not allowed to query members of group: ${ID}',
                'replacements': {
                    'ID': str(group),
                }
            })
        # 3. send the reset command with newest members
        self._send_reset_command(group=group, members=members, receiver=sender)
        # no need to response this group command
        return []
