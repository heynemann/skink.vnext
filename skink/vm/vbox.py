import subprocess

from skink.vm import base


class VmManager(base.VmManager):
    def start(self, name):
        command = [
            "VBoxManage",
            "createvm",
            "--name", 
            name, 
            "--register"
        ]
        subprocess.call(command)

    def stop(self, name):
        command = [
            "VBoxManage",
            "unregistervm",
            name,
            "--delete"
        ]
        subprocess.call(command)
