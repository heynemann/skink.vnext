import subprocess

from skink.vm import base


class VmManager(base.VmManager):
    def create(self, name):
        command = [
            "VBoxManage",
            "createvm",
            "--name",
            name,
            "--register"
        ]
        subprocess.call(command)

    def destroy(self, name):
        command = [
            "VBoxManage",
            "unregistervm",
            name,
            "--delete"
        ]
        subprocess.call(command)
