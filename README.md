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

## fasttextとword2vecとの違い
- fasttextはsubword分割という単語の中の一部が近いと近くなる特性がある
<div align="center">
<img width="300px" src="https://cloud.githubusercontent.com/assets/4949982/24544313/c1896590-163d-11e7-80f4-38896daf783b.png">
</div>

<div align="center">図4. 文脈(skip gram)に依存せず近くなるので、好ましく働くことも、好ましくなく働くこともある </div>

<p align="center">
<img width="800px" src="https://cloud.githubusercontent.com/assets/4949982/24544412/235b635e-163e-11e7-90dc-a9297181a7c3.png">
</p>

- Word2Vecで“艦これ”の関連度を計算すると、同じような文脈で用いられる、他のゲームタイトルが多く混じってしまう
- これはメリットなのか、デメリットなのか、使用用途でわかれそう
<p align="center">
<img width="450px" src="https://cloud.githubusercontent.com/assets/4949982/24544559/a86ae308-163e-11e7-88d5-30d27943fc45.png">
</p>

### 単語の演算の違い
- Word2Vecの特徴として、単語の演算が謎理論（理論的な裏付けが無いように見える）で演算できる
- fasttextもベクトル表現なので、足し算・引き算が可能なので比較する
- fasttextとw2vで結果が異なる
<p align="center">
<img width="750px" src="https://cloud.githubusercontent.com/assets/4949982/24544827/bb4ac5e6-163f-11e7-8b4a-2e3f8b171aa7.png">
</p>

## fasttext, word2vecの実践的な使い方
- CNN, RNNなどのディープラーニングの素性とする
- 例えば、100万語で、10単語の文章の判別問題の際、one-hotを利用すると、壊滅的なテンソルサイズになりGPUに乗らない
- そこで意味関係を内包しているという仮説がある、fasttext, w2vを使うことで、256次元程度にシュリンクできる
<p align="center">
<img width="450px" src="https://cloud.githubusercontent.com/assets/4949982/24544957/4352829e-1640-11e7-888e-5cac42855563.png">
</p>

## RNN(or CNN)の出力をfasttext, word2vecの出力に近似して使う場合
- Deep Learningの出力、特にRNNのテキスト生成系のモデルにおいて、出力次元が爆発してしまう問題に対応するため、出力
- 出力をLinear + mean square errorとすることで、直接ベクトルを当てに行くことができる(復元するにはconsine類似度などで逆引きする必要がある)
<p align="center">
<img width="600px" src="https://cloud.githubusercontent.com/assets/4949982/24545540/7b33c590-1642-11e7-96fa-707a248eed53.png">
</p>
