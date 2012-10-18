from skink.worker.vm import base

from sh import VBoxManage


class VmManager(base.VmManager):
    def create(self, name):
        VBoxManage("createvm", "--name", name, register=True)

    def destroy(self, name):
        VBoxManage("unregistervm", name, delete=True)

    def list(self):
        return VBoxManage("list", "vms")
