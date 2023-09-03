# bufap

bufap は Buffalo製の法人無線LANアクセスポイントWAPMシリーズを管理するためのツールおよびクラスです。

## コマンドラインツールとしての使い方

### インストール
zipファイルを解凍する
* bufap-cli.exe コマンドライン版ツール本体
* bufap-gui.exe GUI版ツール本体

### 使用方法

<details>
<summary> bufap-cli.exe </summary>

```text
usage: bufap-cli [-h] {get-conf,gc,read-conf,rc,wireless-monitor,wm,client-monitor,cm,get-syslog,get-all,ga,exec,apply,ap} ...

WAPMシリーズコンフィグツール

positional arguments:
  {get-conf,gc,read-conf,rc,wireless-monitor,wm,client-monitor,cm,get-syslog,get-all,ga,exec,apply,ap}
    get-conf (gc)       設定を取得
    read-conf (rc)      設定を読み込み
    wireless-monitor (wm)
                        無線環境モニタ
    client-monitor (cm)
                        クライアントモニタ
    get-syslog          ログの取得
    get-all (ga)        情報の一括取得
    exec                実行したコマンドの結果を取得
    apply (ap)          設定の一括反映

optional arguments:
  -h, --help            show this help message and exit
```
</details>

