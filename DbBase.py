# 必要モジュールをインポートする
import sqlite3
from openpyxl import load_workbook
from contextlib import closing

# データベースに接続する
conn = sqlite3.connect(r'C:\pg\example.db')
c = conn.cursor()

# テーブルの作成
c.execute('''CREATE TABLE DocLib(intIndex integer, intClusterNo integer,texPaperAbstract text, texCreateDate text,texCahangeDate)''')

# EXCELをOPEN


# # テーブルの作成
# c.execute('''CREATE TABLE users(id real, name text, birtyday text)''')

# # データの挿入
# c.execute("INSERT INTO users VALUES (1, '煌木 太郎', '2001-01-01')")
# c.execute("INSERT INTO users VALUES (2, '学習 次郎', '2006-05-05')")
# c.execute("INSERT INTO users VALUES (3, '牌存 花子', '2017-09-10')")

# ①EXCELのセルをDBに登録

# ②文書を形態素解析して、DBに登録 →　辞書TBLの作成？

# 挿入した結果を保存（コミット）する
conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()