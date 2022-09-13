import subprocess
import os

class i3MGMT:
    def msg(command):
        os.system('i3-msg {}'.format(command))
    def nag(message):
        subprocess.Popen(['i3-nagbar', '-m', message, '-t', 'warning'])
