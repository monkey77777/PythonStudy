import sqlite3
import csv
import os
import datetime

# データベースに接続する
conn = sqlite3.connect(r'C:\pg\example.db')
c = conn.cursor()

# 読み込み
lstImp = []
# メモリテーブルの定義

# データの読み込み(インポートテーブル)　単語辞書の作成
for row in cur.execute('''
select texPaperAbstract 
from impDocLib 
where texLibFlg = 0 
and texDelFlg = 0
'''):
    lstImp.append(row[0])

# データの読み込み(辞書テーブル)　→　単語と回数を紐づけるため。

# 各文書を単語分解

# メモリ辞書に登録。一時ワーク

# インポートテーブルの読み込みフラグを1(更新済み)に変更

# 辞書への書き込み(読み込んだテーブルの)