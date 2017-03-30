# coding: utf-8
from __future__ import print_function
import os
import math
import sys
import glob
import re
import json
import MeCab
from collections import Counter as C
import plyvel
import pickle
import numpy as np
db = plyvel.DB('shadow.ldb', create_if_missing=True)
m = MeCab.Tagger('-Owakati')
cha = MeCab.Tagger('-Ochasen')
def shadow():
  for gi, name in enumerate(glob.glob('out/*')):
    day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
    who = re.search(':\d\d_(.*?$)', name).group(1)
    f = open(name,'r')
    c = json.loads(f.read())
    try:
      favs = c['favs']
      fr   = c['fr']
      txt  = c['txt']
    except:
      continue
    oneshot = {'___META_FR___':fr, "___META_ID___%s"%who:1 }
    oneshot.update(dict(C(m.parse(txt).strip().split())) )
    db.put(bytes(name.split('/')[-1], 'utf-8'), pickle.dumps(oneshot))
    if gi % 1000 == 0:
      print(gi, day, name)
      print(favs, oneshot)

def test():
  for url, oneshot in db:
     url     = url.decode('utf-8')
     oneshot = pickle.loads(oneshot)
     print(url, oneshot)

# この時のiterは停止する
def w2v():
  date_txts = {}
  for gi, name in enumerate(glob.glob('out/*')):
    day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
    who = re.search(':\d\d_(.*?$)', name).group(1)
    f = open(name,'r')
    c = json.loads(f.read())
    try:
      favs = c['favs']
      fr   = c['fr']
      txt  = c['txt']
    except:
      continue
    if date_txts.get(day) is None: date_txts[day] = []
    date_txts[day].append( m.parse(txt).strip().replace('# ', '#') )
    if gi % 1000 == 0:
      print(gi)
  os.system('rm result/*')
  for date, txts in filter(lambda x:len(x[1]) > 100000, date_txts.items()):
    open('result/_%s_len_%d.txt'%(date, len(txts)), 'w').write( '\n'.join(txts) )
  
  for name in glob.glob('result/*.txt'):
    os.system( './fasttext skipgram -input %s -output %s.model'%(name, name.split('.')[0]) )

# わがままプリンセス
def wagamama():
  term_freq = {}
  for gi, name in enumerate(glob.glob('out/*')):
    if gi % 1000 == 0:
      print("now iter %d"%gi, file=sys.stderr)
    day = re.search('out/(.*?_.*?_.*?)_(.*?$)', name).group(1)
    who = "@%s"%re.search(':\d\d_(.*?$)', name).group(1)
    with open(name,'r') as f:
      try:
        c = json.loads(f.read())
      except json.decoder.JSONDecodeError as e:
        continue
    try:
      favs = c['favs']
      fr   = c['fr']
      txt  = c['txt']
    except:
      continue
    arr = m.parse(txt).strip().split()
    #arr.insert(len(arr)//2, who)
    #to_w2v = ' '.join(arr)
    #print(to_w2v)
    for a in arr:
      if term_freq.get(a) is None:
         term_freq[a] = 0.
      term_freq[a] += 1.
  open('term_freq.pkl', 'wb').write(pickle.dumps(term_freq))
#wagamama()
# 辛い
from scipy import spatial
import itertools 
def relevancy():
  term_freq = {}
  for gi, name in enumerate(glob.glob('result/*.txt')):
    day = re.search('_(.*?_.*?_.*?)_(.*?$)', name).group(1)
    for term, freq in dict(C(open(name, 'r').read().replace('\n', '').split())).items():
      if term_freq.get(term) is None: term_freq[term] = 0
      term_freq[term] += freq

  intersection = None
  for gi, name in enumerate(glob.glob('result/*.vec')):
    buff = set()
    for line in open(name, 'r').read().split('\n')[1:-1]:
       w = line.split()[0]
       buff.add(w)
    if intersection is None:
      intersection = buff
    else:
      intersection = intersection & buff 
  intersection = list(intersection)
  intersection.remove('∬')
  for i in intersection:
    #print(i)
    pass
  for term, freq in sorted(term_freq.items(), key=lambda x:x[1]*-1):
    #print(term, freq)
    pass
  day_term_vec = {}
  for gi, name in enumerate(glob.glob('result/*.vec')):
    day = re.search('_(.*?_.*?_.*?)_(.*?$)', name).group(1)
    print(day)
    data = iter(filter(lambda x:''!=x, open(name, 'r').read().split('\n')))
    for d in data:
      es = d.split()
      term = es.pop(0)
      try:
        es = np.array(list(map(float, es)))
      except:
        continue
      if day_term_vec.get(day) is None: day_term_vec[day] = {}
      day_term_vec[day][term] = es
 
  #for term, freq in sorted(term_freq.items(), key=lambda x:x[1]*-1):
  for term, freq in [('プレミアムフライデー', term_freq['プレミアムフライデー']), \
    ('ｗｗｗｗｗ', term_freq['ｗｗｗｗｗ'])]:
    if '固有名詞' not in cha.parse(term):
      continue
    if term not in intersection:
      continue
    buff = [] 
    for day, term_vec in day_term_vec.items():
      neo = list(map(lambda x:1 - spatial.distance.cosine(term_vec[x], term_vec[term]), intersection))
      buff.append( (day, neo) )
    buff = sorted(buff, key=lambda x:x[0])
    for i in range(len(buff) - 1):
      t1, t2 = buff[i], buff[i+1]
      delta = np.array(t1[1]) - np.array(t2[1])
      print("%s %s <-> %s 変化量 %03f"%(term, t1[0], t2[0], np.linalg.norm(delta) - 11.0) )

    #print(day, "ramen", list(neo))
    #term_vec['ラーメン'] 
if __name__ == '__main__':
  if '--shadow' in sys.argv:
    shadow()
  if '--test' in sys.argv:
    test()
  if '--w2v' in sys.argv:
    w2v()
  if '--rel' in sys.argv:
    relevancy()
