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
        print("MainControl:set_commands")
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

        print("start WaitDialog")
        dlg = WaitDialog("処理中", 60)

        print("start scan_thread")
        thread1 = threading.Thread(target=self.get_info, args=(dlg,))
        thread1.start()

    def get_info(self, dlg):
        print("start get_info")

        print("start scan_wm")
        self.logic.scan_wm()

        print("update conf")
        dlg.set_text("設定取得中")
        self.main_view.conf_view.update_data(self.logic.get_conf())

        print("update cm")
        dlg.set_text("クライアントモニタ取得中")
        self.main_view.cm_view.update_data(self.logic.get_cm())

        print("wait scan wm")
        dlg.set_text("無線環境モニタ取得中")
        while not dlg.end_flg:
            time.sleep(0.5)

        print("update wm")
        self.main_view.wm_view.update_data(self.logic.get_wm())

        print("close dialog")
        dlg.destroy()

        print("end get_info")


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
        level=logging.WARN,
        format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d %(funcName)s] %(message)s",
        stream=sys.stdout,
    )

    control = MainControl()
