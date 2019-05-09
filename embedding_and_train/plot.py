# coding=utf-8

from matplotlib import pyplot

from sklearn.decomposition import PCA
from gensim.models import word2vec
from gensim import models
pyplot.rcParams['font.sans-serif']=['SimHei']  #正常显示中文标签
# load the embedding_and_train model
model = models.Word2Vec.load('word2vec.model')
X = model[model.wv.vocab]

# reduce the dimension of word vector
pca = PCA(n_components=2)
result = pca.fit_transform(X)

pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
