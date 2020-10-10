import sqlite3
import csv
import os
import datetime

# 現在日付セット
d_Today = datetime.date.today()
if len(str(d_Today.month)) == 1:
    strMonth = '0' + str(d_Today.month)
else:
    strMonth = str(d_Today.month)

if len(str(d_Today.day)) == 1:
    strDay = '0' + str(d_Today.day)
else:
    strDay = str(d_Today.day)

texToday = str(d_Today.year) + strMonth + strDay

# インデックスの抽出


#######↓ここのパラメータを変える↓#######
dbname = r'C:\pg\example.db'
target_table_name = 'impDocLib'
import_table_name = r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\04.db\to_csv_outX.csv'
is_create_table = True
is_header_skip = False
#####################################


#######↓インポート先のテーブルDDL↓#######
sql_script = """
    CREATE TABLE impDocLib(intIndex integer, intCluster integer, texPaperAbstract text,texLibFlg text,texDelFlg text, texCreDate text)
"""
#######################################

class ImportSQLite():
    def __init__(self, dbname, target_table_name, import_data_name, is_create_table, is_header_skip=False, sql_create_table=None):
        """
        csvまたはtsvファイルをSQLiteへインポートする
        :param dbname: text 接続先DB名
        :param target_table_name: text インポート先となるDB上のテーブル名
        :param import_data_name: text インポートしたいデータ名
        :param is_create_table: boolean インポート先となるテーブルを作成するか否か
        :param is_header_skip: boolean インポートするデータのヘッダーを読み飛ばすか否か
        :param sql_create_table: text インポート先となるテーブルのDDL
        """
        self.dbname = dbname
        self.target_table_name = target_table_name
        self.import_data_name = import_data_name
        self.is_create_table = is_create_table
        self.is_header_skip = is_header_skip
        _, raw_delimiter = os.path.splitext(import_data_name)
        if raw_delimiter == '.csv':
            self.delimiter = ','
        elif raw_delimiter == '.tsv':
            self.delimiter = '\t'
        else:
            raise ValueError('Import file should be csv or tsv.')

        if is_create_table:
            if not sql_create_table:
                raise ValueError('It\'s necessary of sql to create table')
            else:
                self.sql_create_table = sql_create_table


    def read_import_file(self,intPreIndex):
        with open(self.import_data_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            for row in reader:
                # lstReader の一列目にintIndexを追加する。
                    intPreIndex += 1
                    row.insert(0,intPreIndex)
                # lstReader の最終列に削除フラグ、texCreDateを追加する。
                    row.append('0')
                    row.append('0')
                    row.append(texToday)
            if self.is_header_skip:
                header = next(reader)

            return [i for i in reader]


    def pick_column_num(self, import_data):
        """
        インポートファイルの列数を算出する
        :param import_data: array(two-dimensional)
        :return: int
        """
        columns = []
        for raw in import_data:
            columns.append(len(raw))
        if len(set(columns)) == 1:
            return columns[0]
        else:
            raise ValueError('this import files has diffrenect column numbers.')

    # ポイント???としている部分は、第二引数input_fileから
    def insert_csv_file(self):
        input_file = self.read_import_file(intPreIndex)
        column = self.pick_column_num(input_file)
        val_questions = ['?' for i in range(column)]
        # インデックスと現在日付を追加
        cur.executemany("insert into {0} values ({1})".format(self.target_table_name,','.join(val_questions)), input_file)


if __name__ == '__main__':

    sql = ImportSQLite(
        dbname=dbname,
        target_table_name=target_table_name,
        import_data_name=import_table_name,
        is_create_table=is_create_table,
        is_header_skip= is_header_skip,
        sql_create_table=sql_script
    )

    conn = sqlite3.connect(sql.dbname)
    cur = conn.cursor()

    # インデックスの抽出
    for row in cur.execute('select max(rowId) from impDocLib'):
        if row[0] is None:
            intPreIndex = 0
        else:
            intPreIndex = row[0]

    if sql.is_create_table:
        # 既存テーブルがある場合、削除し新規作成している。
        cur.execute('drop table if exists {};'.format(target_table_name))
        cur.execute(sql.sql_create_table)

    sql.insert_csv_file()

    conn.commit()
    conn.close()
