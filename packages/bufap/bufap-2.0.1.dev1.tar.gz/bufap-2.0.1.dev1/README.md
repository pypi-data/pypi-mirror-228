# bufap

bufap は Buffalo製の法人無線LANアクセスポイントWAPMシリーズを管理するためのツールおよびクラスです。

## コマンドラインツールとしての使い方

### インストール
zipファイルを解凍する
* bufap-cli.exe コマンドラインツール本体
* bufap-getall.bat コマンドラインツールを使って無線APの情報をすべて取得するバッチプログラム

### 使用方法

<details>
<summary> bufap-cli.exe </summary>

```text
usage: bufap-cli.exe [-h] (--get-conf | --read-conf | --wireless-monitor | --client-monitor | --exec) [--host HOST] [--username USERNAME] [--password PASSWORD] [--infile INFILE] [--outfile OUTFILE] [--summarize {yes,no}]
                    [--column {user,default}] [--format {raw,text,dict,csv}] [--command COMMAND]

WAPMシリーズコンフィグツール

options:
  -h, --help            show this help message and exit
  --get-conf            設定を取得
  --read-conf           設定を読み込み
  --wireless-monitor    無線環境モニター
  --client-monitor      クライアントモニター
  --exec                コマンド実行の結果を取得
  --host HOST           ホストアドレス(IP)
  --username USERNAME   ユーザー名
  --password PASSWORD   パスワード
  --infile INFILE       設定ファイルのパス
  --outfile OUTFILE     出力先ファイルのパス
  --summarize {yes,no}  ユーザーが変更した部分のみ表示するかどうか
  --column {user,default}
                        出力するカラムを指定
  --format {raw,text,dict,csv}
                        設定ファイルの場合：raw(APの設定値そのまま),text(必要な情報に絞った表示),dict(辞書形式)
                        クライアントモニタ、無線環境モニタの場合：raw(APの出力そのまま。csv(CSV形式)
  --command COMMAND     exec コマンド指定時のコマンドを実行する
```
</details>

<details>
<summary> bufap-getall.bat </summary>

先頭に記載されているAPのアドレス、ユーザー名、パスワードを書き換えて実行すると、
バッチファイルのあるフォルダに outputフォルダを作成し以下のファイルが保存される。

* %HOST%-config.txt
* %HOST%-status.txt
* %HOST%-syslog.txt
* %HOST%-client.csv
* %HOST%-wireless.csv
  
```text
usage: bufap-getall.bat
```

| :warning: 無線環境モニタを実行するので端末が切断されます |
|--------------------------------------------------------|
</details>