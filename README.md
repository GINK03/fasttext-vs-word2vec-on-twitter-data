# Fasttext vs word2vec survay documents(2017)
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
<div align="center">図1. ある目的の単語から、周辺の単語の確率を計算していってベクトル化する</div>
- Word2vecとfasttextではこれを実装したもの
- 
