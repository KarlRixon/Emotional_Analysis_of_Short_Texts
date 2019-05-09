# -*- coding: utf-8 -*-

from gensim import models
import numpy as np
import logging
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

k = 10  # 人为规定的一个句子包含词数（多退少补）
input_dim = 463 # 词汇表大小，初始化嵌入层时要加一，多一个全0的词向量
output_dim = 50 # 词向量维度
comment_dim = 2496  # 评论条数
batch_size = 32

def count():        # 统计必要信息
    # 载入word2vec模型
    model = models.Word2Vec.load('word2vec.model')
    words = 0
    for _ in model.wv.index2word:
        words += 1
    print("词汇数：", words)

    # 统计评论信息
    f = open("result_cut.txt", encoding='UTF-8')
    line_count = 0
    word_count = 0
    for line in f:
        line_count += 1
        word_count += len(line.split())
    f.close()
    print("评论数：", line_count, " 总词数：", word_count, " 每条评论平均词数：", word_count / line_count)
    return words, line_count

def pad_seq():      # 生成pad_sequences处理数据(x_train)
    # 载入word2vec模型
    model = models.Word2Vec.load('word2vec.model')

    # 建立字典
    word_dict = {}
    index = 0
    for word in model.wv.index2word:
        word_dict.update({word:index})
        index += 1
    # print(word_dict)

    # 设置训练数据为comment_dim*k的矩阵
    all_data = np.zeros((comment_dim, k), dtype=int)
    with open("result_cut.txt", 'r', encoding='UTF-8') as f:
        for line_index, line in enumerate(f.readlines()):
            tmp = line.split()
            if len(tmp) > k:
                tmp = tmp[-k:]  # 截取后k个词语
            for word_index, word in enumerate(tmp):
                if word in model:
                    all_data[line_index][word_index] = word_dict[word]
    all_data = pad_sequences(all_data, maxlen=k, padding='post', truncating='pre', dtype=float)
    # print(all_data)
    return all_data

def my_init(shape): # 生成嵌入层初始化数据
    # 载入word2vec模型
    model = models.Word2Vec.load('word2vec.model')

    emb_init_data = np.zeros(shape, dtype=float)
    for index in range(input_dim):
        emb_init_data[index] = model[model.wv.index2word[index]]
    # emb_init_data[input_dim] = np.zeros(output_dim)     # 添加一个全0词向量
    return emb_init_data

def star():
    comment_star = np.loadtxt("comment_star.txt")
    emotion = []
    for s in comment_star:
        if s <= 3:
            emotion.append(0)
        else:
            emotion.append(1)
    # print(emotion)
    return emotion

def set_data(x, y):     # 8:2的训练集和测试集   正负情感的数据需要混合
    cut = int(comment_dim*0.1)
    mid = int(comment_dim*0.5)
    x_train = np.zeros(((mid-cut)*2, k), dtype=int)
    x_test = np.zeros((cut*2, k), dtype=int)
    y_train = np.zeros(((mid-cut)*2), dtype=int)
    y_test = np.zeros(cut*2, dtype=int)
    for i in range(cut):
        for j in range(k):
            x_test[i*2][j] = x[i][j]
            x_test[i*2+1][j] = x[mid+i][j]
        y_test[i*2] = y[i]
        y_test[i*2+1] = y[mid+i]
    for i in range(mid-cut):
        for j in range(k):
            x_train[i*2][j] = x[cut+i][j]
            x_train[i*2+1][j] = x[mid+cut+i][j]
        y_train[i*2] = y[cut+i]
        y_train[i*2+1] = y[mid+cut+i]
    return x_train, y_train, x_test, y_test

def main():
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    count()
    x_train = pad_seq()
    y_train = star()
    x_train, y_train, x_test, y_test = set_data(x_train, y_train)
    model = Sequential()
    model.add(Embedding(input_dim=input_dim+1, output_dim=output_dim, input_length=k, embeddings_initializer=my_init))
    model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, activation='sigmoid'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1,activation='sigmoid'))
    model.summary()
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=15)
    score, acc = model.evaluate(x_test, y_test, batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)

    predict = model.predict(pad_seq())
    f = open("predict.txt", "w+")
    for i in predict:
        if i > 0.5:
            f.write(str(1)+'\n')
        else:
            f.write(str(0)+'\n')
    f.close()

if __name__ == "__main__":
    main()