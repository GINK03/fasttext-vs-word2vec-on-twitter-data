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

## 応用例：言葉の進化(バズ)を観測する
- 言葉はバズると使用法が変化する
- 今までの主流は単語の出現頻度の変化の観測
- 単語の使われ方の変化を観測する
<p align="center">
<img width="450px" src="https://cloud.githubusercontent.com/assets/4949982/24545646/e78fc98c-1642-11e7-8e02-174a00d4bc96.png">
</p>

- 2次元にエンベットされていると仮定すると、図のようになる
<p align="center">
<img width="180px" src="https://cloud.githubusercontent.com/assets/4949982/24545715/3b69c616-1643-11e7-8186-78444a27af61.png">
</p>
- さらに時間系列でベクトルを表現すると下図のようになる
<p align="center">
<img width="720px" src="https://cloud.githubusercontent.com/assets/4949982/24545746/60927492-1643-11e7-86dc-d0637e7d76f1.png">
</p>

- 技術的な課題点の解決  
-- 問題点:エンベッティングの際、初期値依存性があり、ベクトルが回転したり、端によったりすると歪んだりする。  
-- 解決策:絶対座標に変換するため、基準となる単語を選択（16000単語前後）  
-- 解決策:基準となる単語郡からのコサイン類似度の変化量を各観測したい単語ごとに作成  
-- 解決策:このベクトルをZとする  
<p align="center">
<img width="750px" src="https://cloud.githubusercontent.com/assets/4949982/24545875/00a9cf70-1644-11e7-9a99-49af43db450a.png">
</p>

- Z(プ)ベクトル（長いので略す）をデイリーで作成していき、n日のZ(プ)ベクトルをZ(プ,n)ベクトルとする
- Z(プ,n)ベクトルとZ(プ,n-1)ベクトルとのユークリッド距離を計算する
<p align="center">
<img width="350px" src="https://cloud.githubusercontent.com/assets/4949982/24546027/8aa374c4-1644-11e7-88ba-0b22357ef421.png">
</p>
<div align="center">Dの大きさが大きいほど、使用法が変化したと考えることができ、バズや言葉の進化を定量的に観測することができる。
</div>

- これを日にちのタイムシリーズでグラフを描画すると下図のようになる
<p align="center">
<img width="450px" src="https://cloud.githubusercontent.com/assets/4949982/24546190/16e3da46-1645-11e7-916c-fbdcbf106ce0.png"> 
</p> 

<div align="center">例えば、意味の変化量が少ない「ソシャゲ」という単語と、激しく文脈が変化した「プレミアムフライデー」という単語の変化量Dは大きく違う</div>

# Tweet取得・分析のシステム構成
<p align="center">
<img width="650px" src="https://cloud.githubusercontent.com/assets/4949982/24546324/af3ba68e-1645-11e7-83bd-0154bbc73904.png">
</p>

# Appendix.1. 対応関係を学ぶ
- 図を見ると企業と企業の代表者の関係をみると、一定の法則があることがわかる
<p align="center">
<img width="400px" src="https://cloud.githubusercontent.com/assets/4949982/24546432/38320dd4-1646-11e7-85cc-95dba0e3893c.png">
</p>
- この性質（Distributional inclusion hypothesis）を利用して、logistic-regressionなどで、関係を学習することが可能である

# Appedix.2. 未知の言語を翻訳する
- 出現する単語の並びの関連に相関があるので、言語が異なっても似たような分布になる
<p align="center">
<img width="400px" src="https://cloud.githubusercontent.com/assets/4949982/24546497/8015d2ca-1646-11e7-9bf7-9a2a2c3493bf.png">
</p>
<div align="center"> 文字の文化が共通していれば、翻訳可能？</div>
