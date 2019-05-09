# coding: UTF-8

import jieba
import json

stop_words = []
with open("./stopwords.txt","r") as f:
    for stop_word in f.readlines():
        stop_words.append(stop_word.strip())

with open("./comment_star.txt", "w", encoding='UTF-8') as star_f:
    with open("./result_cut.txt", "w", encoding='UTF-8') as dump_f:
        with open("./result.json", "r", encoding='UTF-8') as load_f:
            comments = json.load(load_f)
            for comment in comments:
                # 分词
                comment_cut = jieba.cut(comment['comment_con'].strip())
                # 引入停用词
                for word in comment_cut:
                    if word not in stop_words:
                        dump_f.write(word.strip()+" ")

                dump_f.write("\n")
            for comment in comments:
                star = comment['comment_star']
                star_f.write(str(star)+'\n')