#
# CommandStop.py
# Botpy
#
# Created by Ashish Ahuja on 5th September 2017.
#
#

from Command import *
import Utilities

class CommandStop(Command):
    def usage():
        return ['stop', 'shutdown']

    def run(self):
        self.reply("Shutting down...")
        Utilities.should_shutdown = True
