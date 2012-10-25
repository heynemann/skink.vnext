#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012 Bernardo Heynemann

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import sys
import os.path
import time

import libvirt
from sh import lxc_create, lxc_stop, lxc_destroy, lxc_list, ssh, ping, arp
from colorama import Fore, Style

from skink.models.config import Config

sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", 0)

aggregated = ''
output = []

def ssh_interact(char, stdin):
    global aggregated

    last_output = ''

    sys.stdout.write(char.encode())
    aggregated += char

    if aggregated.endswith('password: ') or aggregated.endswith('password for ubuntu: '):
        stdin.put("ubuntu\n")

    if (char == '\n'):
        output.append({
            'type': 'out',
            'message': aggregated.replace(last_output, '')
        })
        last_output = aggregated

class LibVirtManager:
    def __init__(self, name):
        self.name = name
        self.clean_output()
        self.connection = libvirt.open("lxc:///")
        self.domain = None
        self.mac = '52:54:00:4d:2b:cd'

        self.lxc_create = lxc_create.bake(_tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)
        self.lxc_stop = lxc_stop.bake(_tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)
        self.lxc_destroy = lxc_destroy.bake(_tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)
        self.lxc_list = lxc_list.bake(_tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)
        self.ping = ping.bake(_tty_in=True, _tty_out=True, _err_to_out=True)
        self.ssh = ssh.bake(_tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)
        self.arp = arp.bake("-an", _tty_in=True, _tty_out=True, _err_to_out=True, _iter=True)

    def find_machine_ip(self):
        ips = self.arp().split('\n')
        for ip in ips:
            if self.mac in ip:
                match = re.match(r'.*\((?P<ip>(?:\d+[.]?)+)\).*', ip)
                if not match:
                    return None
                return match.groupdict()['ip']
        return None

    def log(self, message, message_type="text"):
        global output

        output.append({
            'type': message_type,
            'message': message
        })

        color =''
        if message_type == 'cmd':
            color = Fore.YELLOW + Style.BRIGHT
        print "%s[%s] %s%s" % (color, message_type, message, Style.RESET_ALL)

    def cmd(self, message):
        self.log(message, message_type='cmd')

    def out(self, message):
        self.log(message, message_type='out')

    def br(self):
        self.log('', message_type='br')

    def clean_output(self):
        global output
        output = []

    def cleanup(self):
        self.destroy()

    def bootstrap(self):
        pass

    def get_definition(self):
        xml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libvirt.xml'))
        with open(xml_path, 'r') as xml:
            return xml.read() % {
                "name": self.name,
                "mac": self.mac
            }

    def create(self):
        self.destroy()

        create_cmd = 'lxc-create -t ubuntu -n %s' % self.name
        self.cmd(create_cmd)
        for line in self.lxc_create('-t', 'ubuntu', '-n', self.name, '--', '-S', '/root/.ssh/id_rsa.pub'):
            self.out(line)

        self.domain = self.connection.defineXML(self.get_definition())
        self.domain.create()

        if not self.wait_for_vm_to_boot():
            raise ValueError("VM not booted in time")

    def destroy(self):
        try:
            self.domain = self.connection.lookupByName(self.name)
        except:
            pass

        if self.domain:
            self.cmd('Destroying domain...')
            self.domain.undefine()
            self.domain.destroy()

        if self.name in self.lxc_list():
            stop_cmd = 'lxc-stop -n %s' % self.name
            self.cmd(stop_cmd)
            for line in self.lxc_stop(n=self.name):
                self.out(line)
            destroy_cmd = 'lxc-destroy -n %s -f' % self.name
            self.cmd(destroy_cmd)
            for line in self.lxc_destroy(n=self.name, f=True):
                self.out(line)

    def wait_for_vm_to_boot(self):
        tries = 30

        self.cmd('finding vm ip address...')
        for i in range(tries):
            ip = self.find_machine_ip()
            if ip is None:
                time.sleep(1)
            else:
                break

        if ip is None:
            return False

        self.ip = ip
        self.cmd('ip address found at {0}! waiting for vm to boot...'.format(ip))

        for i in range(tries):
            try:
                self.ping("-c", "1", self.ip)
                return True
            except:
                continue

        return False

    @property
    def config(self):
        return Config.create_from_file(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.skink.yml')))

    def run_command_in_vm(self, command, cwd=True):
        self.cmd(command)

        if cwd:
            command = 'cd ~/skink-build && %s' % command

        p = ssh('-t', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no', 'ubuntu@%s' % self.ip, command, _out=ssh_interact, _out_bufsize=0, _tty_in=True)
        p.wait()

    def clone_repository(self):
        self.cmd('Cloning repository...')
        self.run_command_in_vm('sudo apt-get install -y aptitude git-core', cwd=False)
        self.run_command_in_vm('git clone https://github.com/heynemann/skink.vnext.git ~/skink-build', cwd=False)

    def provision(self):
        self.br()
        self.cmd('Provisioning...')

        self.clone_repository()

        for command in self.config.install:
            self.run_command_in_vm(command)

    def build(self):
        self.br()
        self.cmd('Building...')

        for command in self.config.script:
            self.run_command_in_vm(command)


if __name__ == '__main__':
    vm = LibVirtManager(name="lxctest")
    try:
        vm.bootstrap()
        vm.create()
        #vm.suspend()
        #vm.resume()
        vm.provision()
        vm.build()
    finally:
        vm.cleanup()

