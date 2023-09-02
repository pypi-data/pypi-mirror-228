import csv
import io
import logging
import re

from bufap.ssh import BUFAPssh
from bufap import common


class BUFAPtool:
    ssh = None

    def __init__(self, hostname, username, password):
        self.ssh = BUFAPssh(hostname, username, password)

    def get(self, command) -> str:
        return self.ssh.get(command)

    def gets(self, commands) -> list:
        return self.ssh.gets(commands)

    def scan_wireless_monitor(self):
        ret = self.get("airset wireless-monitor scan")

    def get_wireless_monitor(self, format="csv") -> list:
        # ret = self.get("airset wireless-monitor scan")
        # common.print_waiting("scanning", 60)
        ret = self.get("airset wireless-monitor show status")

        if format in ["dict"]:
            return self.parse_wireless_monitor(ret)

        if format in ["csv"]:
            fields = [
                "Index",
                "MAC",
                "Vendor",
                "SSID",
                "Channel",
                "Mode",
                "RSSI",
                "Noise",
                "Security",
            ]
            ret_csv = io.StringIO()
            writer = csv.DictWriter(ret_csv, fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.parse_wireless_monitor(ret))
            return ret_csv.getvalue()

    def parse_wireless_monitor(self, output: str) -> list:
        """sample
        87 minutes have passed since the previous scan.

        Index MAC                  SSID                                Channel       Mode            RSSI   Noise  Security
        ---------------------------------------------------------------------------------------------------------------------------------------
        1     84:af:ec:3b:8e:30    takano-wifi                         1             802.11g/n       -24    -95    AES
        2     88:57:ee:6f:db:a3    22_11g_CPSE_HM                      11            802.11g/n       -27    -95    AES
        3     88:57:ee:6f:db:a4    19_11g_CPSE_KH                      11            802.11g/n       -27    -95    AES
        """

        ret = []
        start_flg = False
        for line in output.splitlines():
            if line.startswith("--------------------------------------"):
                start_flg = True
                continue
            if not start_flg:
                continue
            try:
                ret.append(
                    {
                        "Index": line[0:6].strip(),
                        "MAC": line[6:27].strip(),
                        "Vendor": common.mac2vendor(line[6:27].strip()),
                        "SSID": line[27:63].strip(),
                        "Channel": line[63:77].strip(),
                        "Mode": line[77:93].strip(),
                        "RSSI": line[93:100].strip(),
                        "Noise": line[100:107].strip(),
                        "Security": line[107:].strip(),
                    }
                )
            except Exception as e:
                logging.warning(f"{e}")
                logging.warning(f"{line}")

        return ret

    def get_client_monitor(self, format="csv") -> list:
        ret = self.get("airset client-monitor show status")

        if format in ["raw", "text"]:
            return ret

        if format in ["dict"]:
            return self.parse_client_monitor(ret)

        if format in ["csv"]:
            fields = [
                "band",
                "SSID",
                "MAC",
                "Vendor",
                "Tx",
                "Rx",
                "RSSI",
                "connect",
                "idle",
            ]
            ret_csv = io.StringIO()
            writer = csv.DictWriter(ret_csv, fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.parse_client_monitor(ret))

            return ret_csv.getvalue()

        if format in ["list"]:
            ret = []
            for r in self.parse_client_monitor(ret):
                ret.append(r.values())
            return ret

    def parse_client_monitor(self, output: str) -> list:
        ret = []
        start_flg = False
        band = ""
        for line in output.splitlines():
            m = re.match(r"\[\s*(?P<band>\S+)\s*\]", line)
            if m:
                start_flg = True
                band = m.group("band")
                continue

            if not start_flg:
                continue

            if line.startswith("SSID") or line.startswith("----------"):
                continue

            try:
                (ssid, mac, tx, rx, rssi, connect, idle) = line.split()
                vendor = common.mac2vendor(mac)
                ret.append(
                    {
                        "band": band,
                        "SSID": ssid,
                        "MAC": mac,
                        "Vendor": vendor,
                        "Tx": common.convert_to_byte(tx),
                        "Rx": common.convert_to_byte(rx),
                        "RSSI": rssi,
                        "connect": connect,
                        "idle": idle,
                    }
                )
            except Exception as e:
                logging.warning(f"{e}")
                logging.warning(f"{line}")

        return ret

    def exec(self, command):
        ret = self.get(command)

        return ret

    def apply(self, commands):
        ret = self.gets(commands)

        return ret

    def get_syslog(self, format="csv") -> list:
        ret = self.get("show syslog facility all")

        if format in ["raw", "text"]:
            return ret

        if format in ["dict"]:
            return self.parse_log(ret)

        if format in ["csv"]:
            fields = [
                "datetime",
                "facility",
                "message",
            ]
            ret_csv = io.StringIO()
            writer = csv.DictWriter(ret_csv, fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.parse_syslog(ret))

            return ret_csv.getvalue()

    def parse_syslog(self, output: str) -> list:
        """sample
        $ show syslog facility all
        date                  facility       log content
        ------------------------------------------------------------------------
        2023/09/01 14:14:40   WIRELESS      wl1 (2.4GHz): Detect interference(74per) [with Non-802.11] on channel 1.
        2023/09/01 14:11:44   WIRELESS      wl1 (2.4GHz): Detect interference(82per) [with Non-802.11] on channel 1.
        2023/09/01 14:11:33   WIRELESS      wl1 (2.4GHz): Detect interference(76per) [with Non-802.11] on channel 1.
        2023/09/01 14:07:04   WIRELESS      wl1 (2.4GHz): Detect interference(76per) [with Non-802.11] on channel 1.
        """

        ret = []
        start_flg = False
        band = ""
        for line in output.splitlines():
            if line.startswith("----------"):
                start_flg = True
                continue

            if not start_flg:
                continue

            try:
                ret.append(
                    {
                        "datetime": line[0:19],
                        "facility": line[22:30].strip(),
                        "message": line[36:].strip(),
                    }
                )
            except Exception as e:
                logging.warning(f"{e}")
                logging.warning(f"{line}")

        return ret
