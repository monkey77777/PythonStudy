import requests
from bs4 import BeautifulSoup
from time import sleep
# coding: utf-8
import MeCab
  #coding: UTF-8
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import collections
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt

with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana.txt', 'r',encoding="utf-8_sig") as f2:
  # 文書ごとに単語を分割してリストにする。
  #ポイント：文書で1区切りになっている。【文書1,文書2,文書3,文書4...】
  trainings = [TaggedDocument(words = data.split(),tags = [i]) for i,data in enumerate(f2)]
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

#for w in trainings[1].words

#print
#print(m.vector.vectors_docs)
doc_vecs = m.docvecs.vectors_docs
def hierarchical_clustering(emb, threshold):
    # 階層型クラスタリングの実施
    # ウォード法 x ユークリッド距離
    linkage_result = linkage(emb, method='ward', metric='euclidean')
    # クラスタ分けするしきい値を決める
    #クラスタリングするユークリッド距離の基準
    threshold_distance = threshold * np.max(linkage_result[:, 2])
    # クラスタリング結果の値を取得
    clustered = fcluster(linkage_result, threshold_distance, criterion='distance')
    print("end clustering.")
    return linkage_result, threshold_distance, clustered
def plot_dendrogram(linkage_result, doc_index, threshold):
    # 階層型クラスタリングの可視化
    plt.figure(facecolor='w', edgecolor='k')
    dendrogram(linkage_result, labels=doc_index, color_threshold=threshold)
    print("end plot.")
    plt.savefig(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\hierarchy.png')
def save_cluster(doc_index, clustered):
    doc_cluster = np.array([doc_index, clustered])
    doc_cluster = doc_cluster.T
    doc_cluster = doc_cluster.astype("int64")
    doc_cluster = doc_cluster[np.argsort(doc_cluster[:,1])]
    np.savetxt(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\cluster.csv', doc_cluster, delimiter=",", fmt="%.0f")
    print("save cluster.")
    return doc_cluster
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana.txt', 'r',encoding="utf-8_sig") as f3:
  #doc_vecs = f3.read()
  #doc_vecs = pd.DataFrame(np.random.rand(16*21).reshape(21,16))
  threshold = 0.4
  linkage_result, threshold, clustered = hierarchical_clustering(doc_vecs, threshold=threshold)
  plot_dendrogram(linkage_result=linkage_result, doc_index=list(range(241)), threshold=threshold)
  docs_cluster = save_cluster(list(range(241)), clustered)

#t_counter = [{},{},{},{},{},{},{},{}]
t_counter = []

with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana.txt', 'r',encoding="utf-8_sig") as f2:
  #words_cluster = [TaggedDocument(words = data.split(),tags = [i]) for i,data in enumerate(f2)]
  f2r = f2.read()
  cluster_words = f2r.replace('\n','')

#クラスターをしたまとまりで言葉一つにまとめる
#一つのクラスターの頻出単語の多い5この単語を抽出する

  for c, words in enumerate(cluster_words):
    count = collections.Counter(words)
    t_counter[c] = count
  # 全ての単語の辞書を作成
  all_word = {}
  for c in cluster_words:
    for word in c:
      all_word[word] = 0

  # クラスタ内の単語総数
  sum_in_c = []
  for count in t_counter:
    num = 0
    for i in count.values():
      num += i
    sum_in_c += [num]

  # tf計算
  tf_c = [{},{},{},{},{},{},{},{}]
  for i, count in enumerate(t_counter):
    for key, value in count.items():
      tf_c[i][key] = value/sum_in_c[i]

  # 単語がいくつの文書に出いているか
  for docs in f2:
    words = docs[1].split(" ")
    for word in set(words):
      all_word[word] += 1

  # idfの計算
  import math
  idf_word = {}
  for key, i in all_word.items():
    idf_word[key] = math.log(2000/i + 1)

  # tf-idfの計算
  tf_idf = [{},{},{},{},{},{},{},{}]
  for i, c in enumerate(tf_c):
    for key, value in c.items():
      tf_idf[i][key] = value * idf_word[key]





