import gensim
from gensim.models import Word2Vec
import pickle
import sys
import json

def id_freq():
  id_freq = {}
  with open('./who_is_h.wakati.withusername', 'r') as f:
    for line in f:
      line = line.strip()
      ents = line.split()
      ids  = list(filter(lambda x:x[0]=="@", ents))
      for id in ids:
        if id_freq.get(id) is None: id_freq[id] = 0
        id_freq[id] += 1

  for id, freq in sorted(id_freq.items(), key=lambda x:x[1]*-1):
    print(id, freq)
#id_freq()
def train():
  with open('who_is_h.wakati.nousername', 'r') as f:
    tweets = []
    for ti, tweet in enumerate(f):
      if ti%10000 == 0:
        print('now iter %d'%ti)
      tweets.append( tweet.strip().split() )
  model = Word2Vec(tweets, size=256, window=5, min_count=3, workers=8)
  open('model.nousername.pkl', 'wb').write( pickle.dumps(model) )

def train_username():
  words = set()
  with open('who_is_h.wakati.withusername', 'r') as f:
    tweets = []
    for ti, tweet in enumerate(f):
      if ti%10000 == 0:
        print('now iter %d'%ti)
      #if ti > 100000: break
      tweets.append( tweet.strip().split() )
      [words.add(word) for word in tweet.strip().split() ]
  open('words.withusername.pkl', 'wb').write( pickle.dumps(words, protocol=4) )
  model = Word2Vec(tweets, size=256, window=5, min_count=1, workers=8)
  open('model.withusername.pkl', 'wb').write( pickle.dumps(model, protocol=4) )

def pred():
  model  = pickle.loads(open('./model.word2vec.nousername.pkl?dl=0', 'rb').read())
  while True:
    words = input().split()
    positive = list(filter(lambda x:x[0]!="-", words))
    negative = list(map(lambda x:x.replace("-", ""), filter(lambda x:x[0]=="-", words) ) )
    print(positive)
    print(negative)
    try:
      tuples = model.wv.most_similar(positive=positive, negative=negative)
      print( json.dumps(tuples, ensure_ascii=False, indent=2) )
    except KeyError as e:
      print( "キーが見つかりませんでした" )

def pred_user():
  model  = pickle.loads(open('./model.withusername.pkl', 'rb').read())
  while True:
    words = input().split()
    try:
      tuples = model.wv.most_similar(positive=words)
      print( json.dumps(tuples, ensure_ascii=False, indent=2) )
    except KeyError as e:
      print( "キーが見つかりませんでした" )
if __name__ == '__main__':
  if '--train' in sys.argv:
    train()
  if '--train_username' in sys.argv:
    train_username()
  if '--pred' in sys.argv:
    pred()
  if '--pred_user' in sys.argv:
    pred_user()
