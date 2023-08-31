# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

import time
from typing import Optional, Tuple

from dimsdk import ID
from dimsdk import ReliableMessage

from ..utils import CacheManager
from ..common import LoginDBI, LoginCommand
from ..common.dbi import is_expired

from .dos import LoginStorage


class LoginTable(LoginDBI):
    """ Implementations of LoginDBI """

    def __init__(self, root: str = None, public: str = None, private: str = None):
        super().__init__()
        man = CacheManager()
        self.__login_cache = man.get_pool(name='login')  # ID => (LoginCommand, ReliableMessage)
        self.__login_storage = LoginStorage(root=root, public=public, private=private)

    def show_info(self):
        self.__login_storage.show_info()

    # Override
    def login_command_message(self, user: ID) -> Tuple[Optional[LoginCommand], Optional[ReliableMessage]]:
        """ get login command message for user """
        now = time.time()
        # 1. check memory cache
        value, holder = self.__login_cache.fetch(key=user, now=now)
        if value is None:
            # cache empty
            if holder is None:
                # cache not load yet, wait to load
                self.__login_cache.update(key=user, life_span=128, now=now)
            else:
                if holder.is_alive(now=now):
                    # cache not exists
                    return None, None
                # cache expired, wait to reload
                holder.renewal(duration=128, now=now)
            # 2. check local storage
            cmd, msg = self.__login_storage.login_command_message(user=user)
            value = (cmd, msg)
            # 3. update memory cache
            self.__login_cache.update(key=user, value=value, life_span=600, now=now)
        # OK, return cached value
        return value

    # Override
    def save_login_command_message(self, user: ID, content: LoginCommand, msg: ReliableMessage) -> bool:
        # 1. check old record
        old, _ = self.login_command_message(user=user)
        if isinstance(old, LoginCommand) and is_expired(old_time=old.time, new_time=content.time):
            # command expired
            return False
        # 2. store into memory cache
        self.__login_cache.update(key=user, value=(content, msg), life_span=600)
        # 3. store into local storage
        return self.__login_storage.save_login_command_message(user=user, content=content, msg=msg)
