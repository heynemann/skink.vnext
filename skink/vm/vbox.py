import subprocess

from skink.vm import base


class VmManager(base.VmManager):
    def start(self, name):
        subprocess.call(["VBoxManage", "createvm", "--name", name, "--register"])

    def stop(self, name):
        subprocess.call(["VBoxManage", "unregistervm", name, "--delete"])
