#
# CommandManager.py
# Botpy
#
# Created by Ashish Ahuja on 4th September 2017.
#
#

import chatexchange as ce
import threading

class CommandManager:
    def __init__(self, commands, chat_rooms):
        self.commands = commands
        self.rooms = chat_rooms
        self.running_commands = []

    def run_command(self, command):
        if command.privileges() == 0:
            command_thread = threading.Thread(target=command.run)
            self.running_commands.append([command, command_thread])
            command_thread.start()
            return

        for each_room in self.rooms:
            if each_room.room_id == command.message.room.id:
                if each_room.is_user_privileged(command.message.user.id, command.privileges()):         
                    command_thread = threading.Thread(target=command.run)
                    self.running_commands.append([command, command_thread])
                    command_thread.start()
                    return

        command.reply("You do not have sufficient privileges to run this command.")

    def handle_command(self, message):
        try:
            message_content = message.content.lower().split()
            del message_content[0]
        except AttributeError:
            return

        for command in self.commands:
            command_usage = command.usage()

            usage_index = -1

            for usage in command_usage:
                usage_index += 1
                usage_components = usage.split()
                args = []
                match = True
                last_index = min(len(usage_components), len(message_content))

                for i in range(last_index):
                    content_component = message_content[i]
                    usage_component = usage_components[i]
                
                    if usage_component == '*':
                        args.append(content_component)
                    elif usage_component == '...':
                        #Everything else is arguments
                        temp_index = i
                        while temp_index < len(message_content):
                            args.append(message_content[temp_index])
                            temp_index += 1
                    elif content_component != usage_component:
                        match = False

                    min_count = (len(usage_components) - 1) if (usage_components[-1] == '...') else len(usage_components)
                    if len(message_content) < min_count:
                        match = False

                    if match:
                        for each_room in self.rooms:
                            if each_room.room_id == message.room.id:
                                command_room = each_room
                                break

                        self.run_command(command(self, message, command_room, args, usage_index))
                        return

    def cleanup_finished_commands(self):
        for command, command_thread in self.running_commands:
            if not command_thread.isAlive():
                self.running_commands.remove([command, command_thread]) 
