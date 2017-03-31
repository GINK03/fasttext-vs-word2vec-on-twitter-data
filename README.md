# Fasttext vs word2vec survey documents(2017)
## word2vec, fastTextの差と実践的な使い方

## 目次
- Fasttextとword2vecの差を調査する
- 実際にあそんでみよう
- Fasttext, word2vecで行っているディープラーニングでの応用例
- 具体的な応用例として、単語のバズ検知を設計して、正しく動くことを確認したので、紹介する
- Appendix

## Embeddingの原理
- Skip gramではある特定の単語の前後の単語の出現確率を測定することでベクトル化する
<p align="center">
<img width="600px" src="https://cloud.githubusercontent.com/assets/4949982/24543247/deba1758-1639-11e7-9f89-fc832bc4c347.png">
</p>
<div align="center">図1. ある目的の単語から、周辺の単語の確率を計算してベクトル化する</div>

- Word2vecとfasttextではこれを実装したもの
- ただし、fasttextにはsubwordという仕組みが入っている
<p align="center">
<img src="https://cloud.githubusercontent.com/assets/4949982/24543754/b0fd76b4-163b-11e7-8477-d234dbc0a85f.png">
</p>
<div align="center">図2. softmaxで共起確率を計算する</div>

## あそんでみよう
2017年2~3月のTwitterのデータ3GByteを学習させたデータがあるので、遊んでみよう  
学習、予想用のプログラムをgithubに、学習済みのmodelをpython3のpickle形式でdropboxにおいてある  
<p align="center">
<img width="700px" src="https://cloud.githubusercontent.com/assets/4949982/24543857/0e7e06be-163c-11e7-9543-4faed454b571.png">
</p>

[ファイルが置いてあるDropboxのリンク](https://www.dropbox.com/sh/zebzb00dhl6wl01/AAD2h2b66DvCQ09p3mC7qEzAa?dl=0)

### Word2vecで遊ぶ方法
ただの言葉の相関の他、言語の足し算引き算した結果、何の単語に近くなるか計算できます。
<p align="center">
<img width="750px" src="https://cloud.githubusercontent.com/assets/4949982/24544060/d1b0f5ec-163c-11e7-89d3-b7b659c27cd8.png">
</p>
<div align="center">図3. word2vecの単語ベクトルの足し算引き算の例</div>

### fasttextで遊ぶ方法
ただの言葉の相関の他、言語の足し算引き算した結果、何の単語に近くなるか計算できます。
<p align="center">
<img width="750px" src="https://cloud.githubusercontent.com/assets/4949982/24544155/39a6b420-163d-11e7-8588-2a5c922039e2.png">
</p>

### fasttextとword2vecとの違い
- fasttextはsubword分割という単語の中の一部が近いと近くなる特性がある
<div align="center">
<img width="300px" src="https://cloud.githubusercontent.com/assets/4949982/24544313/c1896590-163d-11e7-80f4-38896daf783b.png">
</div>
