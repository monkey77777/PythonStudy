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

# 本文をダウンロード
# 返り値はtext(分割していない)
def novel_text_dler(url):
  headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
  }
  r = requests.get(url, headers=headers)
  r.encoding = r.apparent_encoding
  soup =  BeautifulSoup(r.text,'html.parser')
  honbun = soup.find_all("div", id="novel_ex")
  novel = ""
  for text in honbun:
    novel += text.text
  sleep(1)
  return novel

def keitaiso(text):
  tagger = MeCab.Tagger("-Ochasen")
  tagger.parse("")
  node = tagger.parseToNode(text)
  word = ""
  pre_feature = ""
  while node:
    # 名詞、形容詞、動詞、形容動詞であるかを判定する。
    HANTEI = "名詞" in node.feature
    HANTEI = "形容詞" in node.feature or HANTEI
    HANTEI = "動詞" in node.feature or HANTEI
    HANTEI = "形容動詞" in node.feature or HANTEI
    # 以下に該当する場合は除外する。（ストップワード）
    HANTEI = (not "代名詞" in node.feature) and HANTEI
    HANTEI = (not "助動詞" in node.feature) and HANTEI
    HANTEI = (not "非自立" in node.feature) and HANTEI
    HANTEI = (not "数" in node.feature) and HANTEI
    HANTEI = (not "人名" in node.feature) and HANTEI
    if HANTEI:
      if ("名詞接続" in pre_feature and "名詞" in node.feature) or ("接尾" in node.feature):
        word += "{0}".format(node.surface)
      else:
        word += " {0}".format(node.surface)
      #print("{0} {1}".format(node.surface, node.feature))
    pre_feature = node.feature
    node = node.next
  return word[1:]

#novelText = novel_text_dler('https://ncode.syosetu.com/n4028fp/')

number = 10
novel = []
for i in range(number):
    url = "https://ncode.syosetu.com/n263{}gg/".format(i + 1)
    novel.append(novel_text_dler(url))

#print(keitaiso(novelText))

#保存する
with open(r'C:\Users\81903\OneDrive\デスクトップ\松本_WORK\novel_ana1.txt', 'w',encoding="utf-8_sig") as f1:
    for v in novel:
        f1.write(keitaiso(v))
        f1.write('\n')
