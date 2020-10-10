# 必要モジュールをインポートする
import sqlite3
from openpyxl import load_workbook
from contextlib import closing
import csv


with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\01.doc2ana\to_csv_outX.csv', newline='',encoding='UTF-8') as csvfile:
    read = csv.reader(csvfile)
    for row in read:
        print(row)

input('押したら終了')
