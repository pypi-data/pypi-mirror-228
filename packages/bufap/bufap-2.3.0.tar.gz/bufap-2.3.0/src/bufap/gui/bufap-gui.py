import ipaddress
import logging
import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import bufap
from bufap import BUFAPconf
from bufap.gui.menubar import Menubar
from bufap.gui.loginbar import Loginbar
from bufap.gui.show_conf import ShowConf
from bufap.gui.common import DispMode
from bufap.gui.client_monitor import ClientMonitor

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class LoginFrame(ttk.Frame):
    def __init__(self, master, model):
        logging.debug("login: __init__")

        super().__init__(master)
        self.model = model

        self.model.hostname = tk.StringVar(value=self.model.hostname)
        self.model.username = tk.StringVar(value=self.model.username)
        self.model.password = tk.StringVar(value=self.model.password)

        tk.Label(master, text="IPアドレス").pack(side=tk.LEFT)
        tk.Entry(master, width=15, textvariable=self.hostname).pack(side=tk.LEFT)

        tk.Label(master, text="ユーザー名").pack(side=tk.LEFT)
        self.entry_username = tk.Entry(
            master, width=15, textvariable=self.username
        ).pack(side=tk.LEFT)

        tk.Label(master, text="パスワード").pack(side=tk.LEFT)
        self.entry_password = tk.Entry(
            master, width=15, textvariable=self.password
        ).pack(side=tk.LEFT)

        self.button = tk.Button(master, text="情報取得")
        self.button.pack(side=tk.LEFT)

    def setButtomCommand(self, command):
        self.button.config(command=command)


class Model:
    hostname = "192.168.17.101"
    username = "admin"
    password = "password"

    def __init__(self):
        pass

    def get_info(self):
        logging.debug("Login: get_info")

        try:
            self.hostname = str(ipaddress.ip_address(self.entry_host.get()))
            self.username = self.entry_user.get()
            self.password = self.entry_passwd.get()
        except:
            return

        logging.debug(
            f"hostname: {self.hostname}, username : {self.username}, password : {self.password}"
        )
        self.conf = BUFAPconf(
            hostname=self.hostname, username=self.username, password=self.password
        )
        self.update_tree()

        tool = bufap.BUFAPtool(self.hostname, self.username, self.password)
        self.cm = tool.get_client_monitor("csv")
        self.disp_client_monitor(self.nb)


class Application(ttk.Frame):
    host = "192.168.17.101"
    user = "admin"
    passwd = "password"
    tree = None
    v_scrollbar = None
    dispMode = DispMode.ALL
    conf = None
    cm = None
    curr_dir = "./"

    def __init__(self, master=None):
        logging.debug("Application: __init__")

        super().__init__(master)

        self.model = Model()

        self.master.geometry("800x400")
        self.master.title("BUFFALO AP configツール")

        f_top = ttk.Frame(self.master)
        f_top.pack(fill="x")
        f_bottom = ttk.Frame(self.master)
        f_bottom.pack(fill="both")

        self.f_login = LoginFrame(f_top, self.model)
        self.f_login.setButtomCommand(self.model.get_info)

        nb = ttk.Notebook(f_bottom)

        self.tab_show_conf = ttk.Frame(nb)
        self.tab_client_monitor = ttk.Frame(nb)

        nb.add(self.tab_show_conf, text="設定表示")
        nb.add(self.tab_client_monitor, text="クライアントモニタ")

        nb.pack(expand=True, fill="both")

        # self.disp_show_conf()
        # self.disp_client_monitor(self.tab_client_monitor)

    def menu_file_open_click(self, event=None):
        logging.debug("menu_file_open_click")

        filename = filedialog.askopenfilename(title="ファイルを開く", initialdir=self.curr_dir)

        try:
            with open(filename, mode="r") as f:
                contents = f.read()
                self.conf = BUFAPconf(contents)
            self.curr_dir = os.path.dirname(filename)

        except FileNotFoundError:
            return False

        self.update_tree()

    def menu_file_saveas_click(self, event=None):
        logging.debug("menu_file_saveas_click")

        filename = filedialog.asksaveasfilename(
            title="名前を付けて保存", initialdir=self.curr_dir
        )
        contents = self.conf.get_conf_as_text("user")
        try:
            with open(filename, mode="w") as f:
                f.write(contents)
            self.curr_dir = os.path.dirname(filename)

        except IOError:
            return False

    def menu_file_clear_click(self, event=None):
        logging.debug("menu_file_clear_click")

        self.delete_tree()

    def menu_disp_useronly_click(self):
        logging.debug("menu_disp_useronly_click")

        if self.dispMode == DispMode.ALL:
            self.dispMode = DispMode.USER_ONLY
        else:
            self.dispMode = DispMode.ALL

        self.update_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
