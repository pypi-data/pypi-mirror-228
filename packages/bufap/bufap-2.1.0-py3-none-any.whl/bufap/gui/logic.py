import bufap
from bufap.gui.views import ConfView


class Logic:
    def __init__(self):
        pass

    def set_auth(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.tool = bufap.BUFAPtool(hostname, username, password)

    def get_conf(self):
        self.conf = bufap.BUFAPconf(
            hostname=self.hostname, username=self.username, password=self.password
        )
        ret = self.conf.parse_as_table(summarize=True)

        return ret

    def get_cm(self):
        ret = [list(r.values()) for r in self.tool.get_client_monitor(format="dict")]

        return ret

    def scan_wm(self):
        self.tool.scan_wireless_monitor()

    def get_wm(self):
        ret = [list(r.values()) for r in self.tool.get_wireless_monitor(format="dict")]

        return ret
