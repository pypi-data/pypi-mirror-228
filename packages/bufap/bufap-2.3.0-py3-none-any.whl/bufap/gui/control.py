import csv
import logging
import sys
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk

from bufap.gui.views import MainView
from bufap.gui.logic import Logic


class MainLogic:
    def __init__(self):
        pass


class MainControl:
    def __init__(self):
        self.logic = Logic()
        root = tk.Tk()
        self.root = root
        root.title("sample1view")
        self.main_view = MainView(root)
        root.geometry("900x500")
        self.set_commands()
        root.mainloop()

    def set_commands(self):
        logging.info("MainControl:set_commands")
        self.main_view.login_view.set_get_info_click_command(
            self.get_info_click_command
        )

    def get_info_click_command(self):
        # tk.messagebox.showinfo("Control", "情報取得ボタンがクリックされました")

        self.logic.set_auth(
            self.main_view.login_view.hostname.get(),
            self.main_view.login_view.username.get(),
            self.main_view.login_view.password.get(),
        )

        logging.info("start WaitDialog")
        dlg = WaitDialog("処理中", 60)

        logging.info("start scan_thread")
        thread1 = threading.Thread(target=self.get_info, args=(dlg,))
        thread1.start()

    def output(self, fname, data):
        try:
            if type(data) == list:
                with open(fname, "w") as f:
                    writerfile = csv.writer(f, lineterminator="\n")
                    writerfile.writerow(data[0].keys())
                    writerfile.writerows([d.values() for d in data])
            else:
                print(f"output2: {type(data)}")
                with open(fname, "w") as f:
                    f.write(data)
            return True
        except Exception as e:
            logging.error(e)
            logging.error(data[0])
            return e

    def get_info(self, dlg):
        host = self.main_view.login_view.hostname.get()

        logging.info("start get_info")

        logging.info("start scan_wm")
        self.logic.scan_wm()

        try:
            logging.info("update conf")
            dlg.set_text("設定取得中")
            conf_data = self.logic.get_conf()
            self.output(f"{host}-config.csv", conf_data)
            self.main_view.conf_view.update_data(conf_data)
        except Exception as e:
            dlg.set_text(e)
            dlg.end_flg = True
            return False

        logging.info("update cm")
        dlg.set_text("クライアントモニタ取得中")
        cm_data = self.logic.get_cm()
        self.main_view.cm_view.update_data(cm_data)
        self.output(f"{host}-client.csv", cm_data)

        logging.info("update syslog")
        dlg.set_text("ログ取得中")
        syslog_data = self.logic.get_syslog()
        self.main_view.syslog_view.update_data(syslog_data)
        self.output(f"{host}-syslog.csv", syslog_data)

        logging.info("update status")
        dlg.set_text("ステータス取得中")
        status_data = self.logic.get_status(format="raw")
        self.output(f"{host}-status.txt", status_data)

        logging.info("wait scan wm")
        dlg.set_text("無線環境モニタ取得中")
        while not dlg.end_flg:
            time.sleep(0.5)

        logging.info("update wm")
        wm_data = self.logic.get_wm()
        self.main_view.wm_view.update_data(wm_data)
        self.output(f"{host}-wireless.csv", wm_data)

        logging.info("end message")
        dlg.set_text("データ取得完了し、ファイルに保管しました。")

        logging.info("end get_info")


class WaitDialog(tk.Toplevel):
    end_flg = False

    def __init__(self, text, sec):
        super().__init__()
        self.sec = sec
        self.create_dialog(text)

    def create_dialog(self, text):
        """モーダルダイアログボックスの作成"""
        self.title("処理中")  # ウィンドウタイトル
        self.geometry("300x200")  # ウィンドウサイズ(幅x高さ)

        # モーダルにする設定
        self.grab_set()  # モーダルにする
        self.focus_set()  # フォーカスを新しいウィンドウをへ移す

        self.label = tk.Label(self, text=text)
        self.label.pack()

        self.progress = tk.IntVar()
        p = ttk.Progressbar(
            self, maximum=self.sec, mode="determinate", variable=self.progress
        )
        p.pack(expand=True, fill=tk.X, padx=20)

        self.progress_countup()

    def progress_countup(self):
        self.progress.set(self.progress.get() + 1)
        if self.progress.get() > self.sec:
            self.end_flg = True
        else:
            self.after(1000, self.progress_countup)

    def set_text(self, text):
        self.label["text"] = text


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d %(funcName)s] %(message)s",
        stream=sys.stdout,
    )

    control = MainControl()
