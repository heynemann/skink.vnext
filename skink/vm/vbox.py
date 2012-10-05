import subprocess

from skink.vm import base

from sh import VBoxManage

class VmManager(base.VmManager):
    def create(self, name):
        VBoxManage("createvm", "--name", name, register=True)

    def destroy(self, name):
        command = [
            "VBoxManage",
            "unregistervm",
            name,
            "--delete"
        ]
        subprocess.call(command)
