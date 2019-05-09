# -*- coding: utf-8 -*-

import logging
from gensim.models import word2vec
from wordcloud import WordCloud

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.LineSentence("./result_cut.txt")
    model = word2vec.Word2Vec(sentences, size=50, window=10, min_count=5)

    #保存模型
    model.save("./word2vec.model")
    model.wv.save_word2vec_format('model.txt','vocab.txt',binary=False)

    #模型获取方式
    # model = word2vec.Word2Vec.load("your_model_name")

    #导出词云
    f = open('./result_cut.txt', 'r', encoding='UTF-8').read()
    font = r'simhei.ttf'
    # font = r'dragon.ttf'
    w = WordCloud(background_color="white", collocations=True, font_path=font, width=1000, height=860, margin=2).generate(f)
    w.to_file("wordcloud.png")

if __name__ == "__main__":
    main()