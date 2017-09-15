#
# ChatRoom.py
# Botpy
#
# Created by Ashish Ahuja on 12th September 2017.
#
#

import chatexchange as ce
from PrivilegeType import *
from PrivilegedChatUser import *

class ChatRoom:
    def __init__(self, client, room_id, function_callback):
        self.room_id = room_id
        self.client = client
        self.function_callback = function_callback
        self.privilege_types = list()
        self.privileged_users = list()

    def join_room(self):
        self.room = self.client.get_room(self.room_id)
        self.room.join()
        print("Joined room '" + self.room.name + "' with room id " + str(self.room_id) + ".")

    def leave_room(self):
        self.room.leave()

    def watch_room(self):
        self.room.watch(self.function_callback)

    def add_privilege_type(self, privilege_level, privilege_name):
        self.privilege_types.append(PrivilegeType(privilege_level, privilege_name))

    def remove_privilege_type(self, privilege_name):
        for each_type in self.privilege_types:
            if each_type.name == privilege_name:
                self.privilege_types.remove(each_type) 

    def add_privileged_user(self, user_id, privilege_type):
        self.privileged_users.append(PrivilegedChatUser(user_id, self.room_id, privilege_type))

    def remove_privileged_user(self, user_id, privilege_type):
        for each_user in self.privileged_users:
            if each_user.user_id == user_id and each_user.privilege_type == privilege_type:
                self.privileged_users.remove(each_user)
                return

    def is_user_privileged(self, user_id, required_level):
        for each_user in self.privileged_users:
            if each_user.user_id == user_id:
                if each_user.level >= required_level:
                    return True

        return False

    def get_privilege_type_by_level(self, privilege_level):
        for each_type in self.privilege_types:
            if each_type.level == privilege_level:
                return each_type

        return None

    def get_privilege_type_by_name(self, name):
        for each_type in self.privilege_types:
            if each_type.name == name:
                return each_type

        return None