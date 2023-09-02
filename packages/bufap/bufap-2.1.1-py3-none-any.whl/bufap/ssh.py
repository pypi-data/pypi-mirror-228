import logging
import time

import paramiko

RECV_SIZE = 1024 * 32


class BUFAPssh:
    ssh = None

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(
                self.hostname,
                22,
                self.username,
                self.password,
                timeout=10,
                look_for_keys=False,
            )
        except:
            raise ValueError("ssh connect failed")

        return self.ssh

    def _close(self):
        self.ssh.close()
        self.ssh = None

    def _get_shell(self):
        shell = self.ssh.invoke_shell(width=256)
        shell.send("")
        time.sleep(1)
        if shell.recv_ready():
            shell.recv(RECV_SIZE)

        return shell

    def _exec(self, command):
        shell = self._get_shell()

        shell.send(f"{command}\n")
        time.sleep(1)

        ret_data = []
        while True:
            if shell.recv_ready():
                recv_data = shell.recv(RECV_SIZE)
                row_data = [
                    row.strip()
                    for row in recv_data.decode("utf-8").splitlines()
                    if row.strip() != ""
                ]

                if len(row_data) == 0:
                    continue

                if len(row_data) == 1 and (command in row_data[0]):
                    row_data = []
                    continue

                if len(row_data) > 1 and (command in row_data[0]):
                    row_data = row_data[1:]

                if "--More--" in row_data[-1]:
                    if len(row_data) > 1:
                        ret_data += row_data[:-1]
                    shell.send(" ")

                elif "$" in row_data[-1]:
                    if len(row_data) > 1:
                        ret_data += row_data[:-1]
                    break

                else:
                    ret_data += row_data

        ret_text = "\n".join(ret_data)

        return ret_text

    def get(self, command):
        try:
            self._connect()
            ret_text = self._exec(command)
        finally:
            self._close()

        return ret_text

    def gets(self, commands):
        ret = []
        try:
            ssh = self._connect()
            for command in commands.splitlines():
                command = command.strip()
                if command != "" and not command.startswith("#"):
                    ret.append(self._exec(command))
        finally:
            self._close()

        ret_text = "\n".join(ret)

        return ret_text
