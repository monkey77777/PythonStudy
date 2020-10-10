#! p
# モジュールのインポート
from bs4 import BeautifulSoup
import requests, time, re, openpyxl
# 関数定義
def get_number_of_papers(query_word):
    '''
    検索キーワードの対象論文数を表示(引数：検索キーワード)
    '''
    URL = "https://saemobilus.sae.org/search/?op=navigatePage&pageNumber=1\
        &conditions%5B0%5D.keyword={0}".format(query_word)
    headers = {"User-Agent":"hoge"}
    resp = requests.get(URL, timeout=5, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(resp.text, "html.parser")
    result = soup.find(class_ = "filter-number").text
    number = re.sub(r"\D", "", result)
    print("対象件数は" + number + "件です．\
        \n取得したい論文数を10件単位で入力してください")
    #取得したい論文数の入力    
    num_str = input(">> ")
    page = int(-(-int(num_str)/10))
    return page
def webscraping(query_word, num):
    '''
    検索キーワードの対象文献数を表示して，ページのソースを返す（引数：検索キーワード）
    '''
    URL = "https://saemobilus.sae.org/search/?op=navigatePage&pageNumber={0}\
        &conditions%5B0%5D.keyword={1}".format(num+1, query_word)
    headers = {"User-Agent":"hoge"}
    resp = requests.get(URL, timeout=5, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup
def get_paper_infomation(src, list_empty):
    '''
    論文番号，タイトル，アブストラクトを返す(引数：ソース，検索キーワード，論文数)
    '''
    # 論文番号の取得
    paper_numbers = src.find_all(class_="paper-number")
    # 各論文のページのソースを取得し，文献番号，タイトル，アブストラクトをリストとして返す
    for papernumber in paper_numbers:
        papernumber = papernumber.text
        URL = "https://saemobilus.sae.org/content/{}".format(papernumber)
        headers = {"User-Agent":"hoge"}
        resp = requests.get(URL, timeout=5, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(resp.text, "html.parser")
        #タイトルの取得
        title = soup.find("h1")
        if title is None:
            title = "取得できませんでした"
        else:
            title = title.text
        #アブストラクトの取得
        abstract = soup.find(class_="htmlview paragraph")
        if abstract is None:
            abstract = "取得できませんでした"
        else:
            abstract = abstract.text
        list_empty.append([papernumber, title, abstract])
    return 0
def datawrite_excel(query_word, list_paper_inforamtion, wb_svpass):
    '''
    Excelに論文番号，タイトル，アブストラクトを出力
    '''
    # ExcelBookの作成
    wb = openpyxl.Workbook()
    sheets = wb.sheetnames
    sheet = wb._sheets[0]
    # Excelsheetの見出しの設定
    title0 = "number of results"
    title1 = "Paper number"
    title2 = "Paper title"
    title3 = "Paper Abstract"
    row_base = 1 
    col_base = 1
    sheet.cell(row = row_base, column= col_base).value = title0
    sheet.cell(row = row_base, column= col_base + 1).value = title1
    sheet.cell(row = row_base, column= col_base + 2).value = title2
    sheet.cell(row = row_base, column= col_base + 3).value = title3
    # データの書き込み
    for i in range(len(list_paper_inforamtion)):
        sheet.cell(row = row_base + i + 1, column= col_base + 1).value = list_paper_inforamtion[i][0]
        sheet.cell(row = row_base + i + 1, column= col_base + 2).value = list_paper_inforamtion[i][1]
        sheet.cell(row = row_base + i + 1, column= col_base + 3).value = list_paper_inforamtion[i][2]
    # ExcelBookの保存，終了
    wb.save(wb_svpass)
    #wb.close()
    return 0
def main():
    '''
    1. 変数の設定(キーワード入力，Excelシートのパス指定)
    2. スクリプトの実行
    '''
    # 変数の設定
    print("キーワードを入力してください")
    query_word = input(">> ")
    wb_svpass = "C:\\Users\\81903\\OneDrive\\デスクトップ\\松本_WORK\\{}.xlsx".format(query_word)
    # リストの作成
    list_empty = []
    # 対象文献数の表示
    page = get_number_of_papers(query_word)
    # 論文情報(論文番号，タイトル，アブストラクト)を取得してリストに追加
    for num in range(page):
        src = webscraping(query_word, num)
        # 論文情報(論文番号，タイトル，アブストラクト)をリストへ追加
        get_paper_infomation(src, list_empty)
        print(str((num+1)*10) + "件処理しました")
    # リストの再定義
    list_paper_information = list_empty
    # Excelへの出力
    datawrite_excel(query_word, list_paper_information, wb_svpass)
    print("終了しました")
#実行
if __name__ == "__main__":
    main()