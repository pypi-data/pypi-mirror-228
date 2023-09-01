#!/usr/bin/env python3

import argparse
import logging
import pprint
import os
import sys
from typing import Union, IO

import bufap
import bufap.common


def _output(output: list, outfile: Union[str, bytes, os.PathLike]) -> None:
    if outfile:
        outfile.write(output)
    else:
        print(output)


def get_conf(args) -> None:
    conf = bufap.BUFAPconf(
        hostname=args.host,
        username=args.username,
        password=args.password,
    )
    output = parse_conf(conf, args.column, args.summarize, args.format)
    _output(output, args.outfile)


def read_conf(args) -> None:
    conf = bufap.BUFAPconf(conf_file=args.infile)

    output = parse_conf(conf, args.column, args.summarize, args.format)
    _output(output, args.outfile)


def parse_conf(
    conf: str,
    column: str,
    summarize: bool,
    format: str,
) -> list:
    if format == "raw":
        output = conf.as_raw()
    elif format == "text":
        conf.parse_as_table(summarize)
        output = conf.as_text(column, summarize)
    elif format == "dict":
        conf.as_dict(column, summarize)
        output = pprint.pformat(conf.conf_dict)

    return output


def wireless_monitor(args) -> None:
    tool = bufap.BUFAPtool(args.host, args.username, args.password)
    tool.scan_wireless_monitor()
    bufap.common.print_waiting("scanning", 60)
    output = tool.get_wireless_monitor(args.format)

    _output(output, args.outfile)


def client_monitor(args) -> None:
    tool = bufap.BUFAPtool(args.host, args.username, args.password)
    output = tool.get_client_monitor(args.format)

    _output(output, args.outfile)


def exec(args) -> None:
    if args.command:
        tool = bufap.BUFAPtool(args.host, args.username, args.password)
        output = tool.exec(args.command)

        _output(output, args.outfile)


def get_all(args) -> None:
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    args.format = "raw"
    args.column = "user"
    args.summarize = False

    fpath = os.path.join(args.outdir, f"{args.host}-config.txt")
    with open(fpath, "w") as f:
        args.outfile = f
        args.command = "show config all"
        exec(args)

    fpath = os.path.join(args.outdir, f"{args.host}-status.txt")
    with open(fpath, "w") as f:
        args.outfile = f
        args.command = "show status all"
        exec(args)

    fpath = os.path.join(args.outdir, f"{args.host}-syslog.txt")
    with open(fpath, "w") as f:
        args.outfile = f
        args.command = "show syslog facility all"
        exec(args)

    args.format = "csv"
    fpath = os.path.join(args.outdir, f"{args.host}-client.csv")
    with open(fpath, "w") as f:
        args.outfile = f
        client_monitor(args)
    fpath = os.path.join(args.outdir, f"{args.host}-wireless.csv")
    with open(fpath, "w") as f:
        args.outfile = f
        wireless_monitor(args)


def apply(args) -> None:
    tool = bufap.BUFAPtool(args.host, args.username, args.password)

    commands = args.infile.read()
    output = tool.apply(commands)

    _output(output, args.outfile)


def parse_args():
    parsers = {}

    parsers["root"] = argparse.ArgumentParser(
        prog="bufap-cli",
        description="WAPMシリーズコンフィグツール",  # 引数のヘルプの前に表示
        add_help=True,  # -h/–help オプションの追加
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parsers["root"].add_subparsers()

    parsers["gc"] = subparsers.add_parser(name="get-conf", aliases=["gc"], help="設定を取得")
    parsers["gc"].set_defaults(handler=get_conf)

    parsers["rc"] = subparsers.add_parser(
        name="read-conf", aliases=["rc"], help="設定を読み込み"
    )
    parsers["rc"].set_defaults(handler=read_conf)

    parsers["wm"] = subparsers.add_parser(
        name="wireless-monitor", aliases=["wm"], help="無線環境モニタ"
    )
    parsers["wm"].set_defaults(handler=wireless_monitor)

    parsers["cm"] = subparsers.add_parser(
        name="client-monitor", aliases=["cm"], help="クライアントモニタ"
    )
    parsers["cm"].set_defaults(handler=client_monitor)

    parsers["exec"] = subparsers.add_parser(name="exec", help="実行したコマンドの結果を取得")
    parsers["exec"].add_argument(
        "--command",
        help="実行するコマンドを指定する",
    )
    parsers["exec"].set_defaults(handler=exec)

    parsers["ga"] = subparsers.add_parser(
        name="get-all", aliases=["ga"], help="情報の一括取得"
    )
    parsers["ga"].set_defaults(handler=get_all)

    parsers["ap"] = subparsers.add_parser(name="apply", aliases=["ap"], help="設定の一括反映")
    parsers["ap"].set_defaults(handler=apply)

    for p in ["wm", "cm"]:
        parsers[p].add_argument(
            "--format",
            choices=["raw", "text", "dict", "csv"],
            default="text",
            help="raw: APの出力そのまま | " "csv: CSV形式",
        )

    for p in ["gc", "rc", "wm", "cm", "exec", "ga", "ap"]:
        parsers[p].add_argument("--host", help="ホストアドレス(IP)")
        parsers[p].add_argument("--username", default="admin", help="ユーザー名")
        parsers[p].add_argument("--password", default="password", help="パスワード")

    for p in ["gc", "rc", "wm", "cm", "exec", "ap"]:
        parsers[p].add_argument(
            "--outfile", type=argparse.FileType("w"), default="-", help="出力先ファイルのパス"
        )

    for p in ["gc", "rc"]:
        parsers[p].add_argument(
            "--format",
            choices=["raw", "text", "dict"],
            default="text",
            help="raw: APの設定値そのまま | text: 必要な情報に絞った表示 | dict: 辞書形式",
        )
        parsers[p].add_argument(
            "--summarize",
            help="ユーザーが変更した部分のみ表示するかどうか",
            action="store_true",
        )
        parsers[p].add_argument(
            "--no-summarize",
            help="ユーザーが変更した部分のみ表示するかどうか",
            action="store_false",
            dest="summarize",
        )

        parsers[p].add_argument(
            "--column", choices=["user", "default"], default="user", help="出力するカラムを指定"
        )

    for p in ["rc", "ap"]:
        parsers[p].add_argument(
            "--infile", type=argparse.FileType("r"), help="設定ファイルのパス"
        )

    for p in ["ga"]:
        parsers[p].add_argument("--outdir", default="output", help="出力先のフォルダを指定")

    args = parsers["root"].parse_args()

    return (parsers, args)


def main() -> None:
    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d %(funcName)s] %(message)s",
        stream=sys.stderr,
    )

    (parsers, args) = parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parsers["root"].print_help()

    sys.exit(0)


if __name__ == "__main__":
    main()
