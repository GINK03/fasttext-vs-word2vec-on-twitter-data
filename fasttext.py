from gensim.models import KeyedVectors
import json
import sys
import pickle
def pred():
  model = pickle.loads(open('fasttext.gensim-model.pkl', 'rb').read())
  while True:
    words = input().split()
    positive = list(filter(lambda x:x[0]!="-", words))
    negative = list(map(lambda x:x.replace("-", ""), filter(lambda x:x[0]=="-", words)) )
    try:
      scores = model.most_similar(positive=positive, negative=negative)
      print( json.dumps(scores, ensure_ascii=False, indent=2) )
    except KeyError as e:
      print( "指定したキーが存在しませんでした" )

def pred_user():
  model = pickle.loads(open('fasttext.withuser.gensim-model.pkl', 'rb').read())
  while True:
    words = input().split()
    try:
      scores = model.most_similar(positive=words)
      print( json.dumps(scores, ensure_ascii=False, indent=2) )
    except KeyError as e:
      print( "指定したキーが存在しませんでした" )
def convert_fasttext2gensim():
  model = KeyedVectors.load_word2vec_format('model.vec', binary=False)
  open('fasttext.gensim-model.pkl', 'wb').write(pickle.dumps(model) )
  model = KeyedVectors.load_word2vec_format('model.withuser.vec', binary=False)
  open('fasttext.withuser.gensim-model.pkl', 'wb').write(pickle.dumps(model) )
  sys.exit()
if __name__ == '__main__':
  if '--pred' in sys.argv:
    pred()
  if '--pred_user' in sys.argv:
    pred_user()
  if '--convert' in sys.argv:
    convert_fasttext2gensim()

