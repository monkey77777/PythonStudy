# 必要モジュールをインポートする
import sqlite3
from openpyxl import load_workbook
from contextlib import closing
import csv

# from openpyxl import load_workbook

# DB変数設定
path = ''
port = ''
dbname = ''
user = ''
password = ''

# 現在日付の変数セット
d_today = datetime.date.today()

# リスト変数定義
r_lst = []

# データベースに接続する
conn = sqlite3.connect(r'C:\pg\example.db')
c = conn.cursor()

# テーブルの作成
c.execute('''CREATE TABLE DocLib(intIndex integer, intCluster integer, birtyday text,date)''')

# ①CSV読み込み
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\01.doc2ana\to_csv_outX.csv', newline='',encoding='UTF-8') as csvfile:
    read = csv.reader(csvfile)
    for row in read:
        print(row)

# メモリテーブルの作成
## with を使ってconnectすることでこのブロック処理が完了時にcloseしてくれる
with closing(sqlite3.connect(':memory:')) as conn:
    cur = conn.cursor()

    sql_tbl = '''create table doclist (
                                    intIndex integer(5)
                                    intClusterNo integer(3),
                                    texPaperAbstract text(20000),
                                    date text(10)
                                    )'''

    cur.execute(sql_tbl)

# INSERT
## cur.execute('insert into doclist values(hogehoge)') でもよい
## 今回はr_lstというリストに1レコード1タプルで複数レコードを格納しているためexecutemanyにて実行
## r_lst = [ (a,b,c), (aa,bb,cc), (aaa,bbb,ccc) ] というような感じの構造
    cur.executemany("insert into doclist values()", r_lst)
    conn.commit()

# # 挿入した結果を保存（コミット）する
 conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()