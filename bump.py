#!/usr/bin/env python3
"""
公開前に必ず実行するスクリプト。

index.html の中の「画像などのファイル」のURLに、
更新した日時の印（?v=202609011740 のような番号）を付け直す。

なぜ必要か：
  ブラウザは一度読み込んだファイルを手元に保存して使い回すため、
  中身を差し替えても古い見た目のままになることがある。
  URLの末尾が変われば「別のファイル」として扱われ、必ず読み直される。

使い方：
  python3 bump.py
"""

import re
import datetime
import pathlib

SITE = "https://mee-profile.lpidentity.workers.dev"
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"

# 印を付ける対象（ローカルのファイルだけ。外部URLには付けない）
TARGET = re.compile(
    r'(?P<attr>(?:href|src|content|poster)=")'
    r'(?P<path>images/[^"?]+|styles\.css|favicon\.svg)'
    r'(?:\?v=\d+)?'
    r'(?P<tail>")'
)

stamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
html = HTML.read_text(encoding="utf-8")


def add_stamp(m):
    return f'{m["attr"]}{m["path"]}?v={stamp}{m["tail"]}'


html, n = TARGET.subn(add_stamp, html)

# OGP画像は、SNSでシェアしたときに絶対URLでないと読まれないため差し替える
html = re.sub(
    r'(<meta property="og:image" content=")[^"]*(")',
    rf'\g<1>{SITE}/images/ogp.jpg?v={stamp}\g<2>',
    html,
)

HTML.write_text(html, encoding="utf-8")
print(f"更新の印を付けました：?v={stamp}（{n}か所）")
