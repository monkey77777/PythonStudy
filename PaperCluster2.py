# モジュールのインポート
from bs4 import BeautifulSoup
import requests, time, re, openpyxl

import MeCab
  #coding: UTF-8
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import collections
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
import math
import pickle
import csv

# プログラム概要
# クラスター化されたエクセルから
# エクセルからクラスター分類値を取得し、その塊単位で行う
# クラスターで1単位と考える。(クラスターがほかのクラスターと比べどのような値が出てくるかを調べる。)

# 変数定義

## 各クラスターの文字の種類の数を格納。(重複数はカウントしない)
t_counter = [{},{},{},{},{},{},{},{},{},{}]
## 辞書格納場所
all_word = {}
all_cluster_words = {}
#　クラスターワード(単語分解)の初期化
# cluster_words = []
# list_doc = []
## クラスターの数を格納するための配列
list_of_cluster = []
##　各クラスターの総数
sum_in_c = []
#　tf_cの定義
tf_c = [{},{},{},{},{},{},{},{},{},{}]
#　idf_wordの定義　
idf_word = {}
#　tf_idfの定義
tf_idf = [{},{},{},{},{},{},{},{},{},{}]

#
# CSVの読込み，データフレームの作成
# 引数で指定したcluster値を一つにセット
def dfset_cluster(cluster_no):
    df = pd.read_csv(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\to_csv_out.csv',encoding='utf-8-sig')
    df = df.query('cluster == {}'.format(cluster_no))
    return df

# クラスター毎にクラスターワードを作成
def cre_clusterwords(cluster_no,df):
    cluster_words = []
    list_doc = []
    # クラスター内の文書を1つずつlist_docに追加
    for idx,row in df.iterrows():
        list_doc.append(row["PaperAbstract"])
    # list_docを1文書ずつ単語分解し、クラスターワードに格納
    for i in range(len(list_doc)):
        cluster_words += list_doc[i].split()
    # 【予定】次の単語をクラスターワードから除外。a in the of to (助詞)
    # クラスター単位でクラスター(言葉の種類)の数を格納
    t_counter[cluster_no] = collections.Counter(cluster_words)
    # クラスターごとに言葉の種類を算出
    list_of_cluster.append(cluster_words)
    return 0

# 辞書の追加
def cre_allword():
    all_cluster_words = []
    for i in range(len(list_of_cluster)):
        # flg_chk = 0 
        for j in range(len(list_of_cluster[i])):
            if detPar(list_of_cluster[i][j]) == 0:
                all_cluster_words.append(list_of_cluster[i][j])
    #単語の種類をすべて格納する
    for word in set(all_cluster_words):
        all_word[word] = 0
    for word in set(all_cluster_words):
        all_word[word] += 1
    return 0

# sum_cluster
def sum_cluster(sum_in_c):
    for count in t_counter:
        num = 0
        # for i in count.values():
        for key,value in count.items():
            if detPar(key) == 0:
                num += value
        sum_in_c += [num]
    return sum_in_c

# tfの計算
# やっていることクラスター単位で単語の出現頻度を調べる
def tf_cal(sum_in_c):
    for i, count in enumerate(t_counter):
        for key, value in count.items():
            if detPar(key) == 0:
                tf_c[i][key] = value/sum_in_c[i]
    return 0

#　助詞を判断
def detPar(key):
    if key != "the":
        if key != "a":
            if key != "to":
                if key != "and":
                    if key != "in":
                        if key != "of":
                            if key != "with":
                                if key != "The":
                                    if key != "are":
                                        if key != "for":
                                            if key != "is":
                                                if key != "on":
                                                    if key != "be":
                                                        if key != "an":
                                                            if key != "by":
                                                                if key != "that":
                                                                    if key != "as":
                                                                        if key != "was":
                                                                            if key != "this":
                                                                                if key != "This":
                                                                                    if key != "has":
                                                                                        if key != "from":
                                                                                            if key != "at":
                                                                                                if key != 'which':
                                                                                                    if key != 'have':
                                                                                                        if key != 'can':
                                                                                                            if key != 'vehicle':
                                                                                                                if key != 'been':
                                                                                                                    if key != 'emission':
                                                                                                                        if key != 'fuel':
                                                                                                                            if key != 'In':
                                                                                                                                if key != 'paper':
                                                                                                                                    if key != 'were':
                                                                                                                                        if key != 'or':
                                                                                                                                            if key != 'A':
                                                                                                                                                if key != 'it':
                                                                                                                                                    if key != 'emissions':
                                                                                                                                                        if key != 'these':
                                                                                                                                                            if key != 'used':
                                                                                                                                                                if key != 'used':
                                                                                                                                                                    if key != 'using':
                                                                                                                                                                        if key != 'compute':
                                                                                                                                                                            if key != 'new':
                                                                                                                                                                                if key != 'make':
                                                                                                                                                                                    if key != 'will':
                                                                                                                                                                                        if key != 'system':
                                                                                                                                                                                            return 0
    return 9

# idfの計算
# tfの逆数
def idf_cal():
    for key, values in all_word.items():
        # 1000は文書の数
        idf_word[key] = math.log(1000/(values + 1))

    return 0

# tf-idfの計算
def tf_idf_cal():
    for i, c in enumerate(tf_c):
        for key, value in c.items():
            tf_idf[i][key] = value * idf_word[key]
    return 0

# 特徴語の上位5つをピックアップしエクセル(またはCSV)に出力


# メイン関数
def main():
    # all_cluster_words = []
    cluster_num = 10
    sum_in_c = []
    # TFIDFの事前準備
    for i in range(cluster_num):
        df = dfset_cluster(i)
        cre_clusterwords(i,df)
    cre_allword()
    # クラスタ内の単語総数
    sum_in_c = sum_cluster(sum_in_c)
    sum_in_c = tf_cal(sum_in_c)
    idf_cal()
    tf_idf_cal()
    # tf_idf_sort = []
    tf_idf_sort = sorted(tf_idf[0].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[1].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[2].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[3].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[4].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])

    tf_idf_sort = sorted(tf_idf[5].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[6].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[7].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[8].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    tf_idf_sort = sorted(tf_idf[9].items(), key=lambda x:x[1])
    print(tf_idf_sort[-6:-1])
    
    print("test")



#実行
if __name__ == "__main__":
    main()