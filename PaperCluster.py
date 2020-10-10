#! p
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

# 関数定義
# 言葉のリスト化
def list_of_words():
    '''
    検索キーワードの対象論文数を表示(引数：検索キーワード)
    '''
    #with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana.txt', 'r',encoding="utf-8_sig") as f2:
    #いずれエクセル名は指定したい
    book = openpyxl.load_workbook(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\TWC.xlsx')
    active_sheet = book.active
    max_row = active_sheet.max_row
    #ループで1次行列に変換
    list_of_document = []
    for i in range(max_row - 2):
        list_of_document.append(active_sheet['D{}'.format(i+2)].value)

    # 文書ごとに単語を分割してリストにする。
    #ポイント：文書で1区切りになっている。【文書1,文書2,文書3,文書4...】
    trainings = [TaggedDocument(words = data.split(),tags = [i]) for i,data in enumerate(list_of_document)]
    #trainings = [print(data) for i,data in enumerate(list_of_document)]
    # 学習の実行
    #dm:1ならPV=DMで0ならPV-DBOWで学習する
    #vector_size:文章を何次元の分散表現に変換するかを指定
    #window:次の単語の予測に何単語を用いるか(PV-DMの場合) 又は、文書idから何単語を予測するか(PV-DBOWの場合)
    #min_count:指定の数以下の出現回数の単語は無視する
    #wokes:学習に用いるスレッド数
    #
    m = Doc2Vec(documents= trainings, dm = 1, size=5, window=5, min_count=3, workers=1)
    # モデルのセーブ
    m.save(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\doc2vec.model')
    # モデルのロード
    m = Doc2Vec.load(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\doc2vec.model')

    doc_vecs = m.docvecs.vectors_docs

    threshold = 0.3
    linkage_result, threshold, clustered = hierarchical_clustering(doc_vecs, threshold=threshold)
    plot_dendrogram(linkage_result=linkage_result, doc_index=list(range(m.corpus_count)), threshold=threshold)
    docs_cluster = save_cluster(list(range(m.corpus_count)), clustered)

    t_counter = [{},{},{}]
    all_word = {}

#     #リストの1行目から言葉を格納する
#     #単語の出現回数
#     for i in range(3):
#         #単語分解
#         cluster_words = list_of_document[i].split()
#         #単語の種類の数
#         t_counter[i] = collections.Counter(cluster_words)
#         #words[len(words):len(words)] = cluster_words

#         #単語の種類をすべて格納する
#         for word in set(cluster_words):
#             all_word[word] = 0
#         # 単語がいくつの文書に出いているか

#     #set(words)：重複をはじく
#     #クラスターに出るたびに加算する
#     for i in range(3):
#         cluster_words = list_of_document[i].split()
#         for word in set(cluster_words):
#             all_word[word] += 1
#     #for docs in list_of_document[0:3]:
#     #words = docs[1].split(" ")

#     # クラスタ内の単語総数
#     sum_in_c = []
#     for count in t_counter:
#         num = 0
#         for i in count.values():
#             num += i
#         sum_in_c += [num]

#     # tf計算
#     tf_c = [{},{},{}]
#     for i, count in enumerate(t_counter):
#         for key, value in count.items():
#             tf_c[i][key] = value/sum_in_c[i]

#     # idfの計算
#     idf_word = {}
#     for key, values in all_word.items():
#         idf_word[key] = math.log(99/values + 1)

#     mylist = []

#     # tf-idfの計算
#     tf_idf = [{},{},{}]
#     for i, c in enumerate(tf_c):
#         for key, value in c.items():
#             tf_idf[i][key] = value * idf_word[key]
#         print(mylist.sort)

#     # tf_c    idf_word    tf_idf
#     # with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster1.csv', 'w',encoding="utf-8_sig") as f1:
#     #     for i in range(8):
#     #         f1.writelines(tf_c[i])
#     # write_csv(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster1.csv',tf_c)

#     d2 = [{} , {} , {}]
#     for i in range(8):
#         for k,v in tf_c[i].items():
#             d2[i][k] = pd.Series(v)
#         print(d2[i])

#     # # with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster2.csv', 'w',encoding="utf-8_sig") as f1:
#     # #     writer = csv.writer(f1)
#     # #     for i in idf_word:
#     # #         writer.writerow(i)
#     # write_csv(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster2.csv',idf_word)

#     with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster3.csv', 'w',encoding="utf-8_sig") as f1:
#         for i in range(8):
#           f1.writelines(tf_idf)
#     write_csv(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster3.csv',tf_idf)
#     # print(idf_word[0])
#     # print(idf_word[1])
#     # print(idf_word[2])

#     # tf_c
#     # d2={}
#     # for k,v in idf_word.items():   # 一度pd.Seriesに変換
#     #     d2[k]=pd.Series(v)

# def hierarchical_clustering(emb, threshold):
#     # 階層型クラスタリングの実施
#     # ウォード法 x ユークリッド距離
#     linkage_result = linkage(emb, method='ward', metric='euclidean')
#     # クラスタ分けするしきい値を決める
#     #クラスタリングするユークリッド距離の基準
#     threshold_distance = threshold * np.max(linkage_result[:, 2])
#     # クラスタリング結果の値を取得
#     clustered = fcluster(linkage_result, threshold_distance, criterion='distance')
#     print("end clustering.")
#     return linkage_result, threshold_distance, clustered

# def plot_dendrogram(linkage_result, doc_index, threshold):
#     # 階層型クラスタリングの可視化
#     plt.figure(facecolor='w', edgecolor='k')
#     dendrogram(linkage_result, labels=doc_index, color_threshold=threshold)
#     print("end plot.")
#     plt.savefig(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\hierarchy.png')

# def save_cluster(doc_index, clustered):
#     doc_cluster = np.array([doc_index, clustered])
#     doc_cluster = doc_cluster.T
#     doc_cluster = doc_cluster.astype("int64")
#     doc_cluster = doc_cluster[np.argsort(doc_cluster[:,1])]
#     np.savetxt(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster.csv', doc_cluster, delimiter=",", fmt="%.0f")
#     print("save cluster.")
#     return doc_cluster

# with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana.txt', 'r',encoding="utf-8_sig") as f2:
#   #words_cluster = [TaggedDocument(words = data.split(),tags = [i]) for i,data in enumerate(f2)]
#   f2r = f2.read()
#   cluster_words = f2r.replace('\n','')

# #クラスターをしたまとまりで言葉一つにまとめる
# #一つのクラスターの頻出単語の多い5この単語を抽出する

# def write_csv(file, save_dict):
#     save_row = {}

#     with open(file,'w') as f:
#         writer = csv.DictWriter(f, fieldnames=save_dict.keys(),delimiter=",",quotechar='"')
#         writer.writeheader()

#         k1 = list(save_dict.keys())[0]
#         length = len(save_dict[k1])

#         for i in range(length):
#             for k, vs in save_dict.items():
#                 save_row[k] = vs[i]

#             writer.writerow(save_row)

def main():
    '''
    1. 変数の設定(キーワード入力，Excelシートのパス指定)
    2. スクリプトの実行
    '''
    list_of_words()
    print("終了しました")
#実行
if __name__ == "__main__":
    main()