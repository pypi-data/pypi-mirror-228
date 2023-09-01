# --------------------------------------------
import logging
from typing import List
import codefast as cf
import jieba
from gensim import corpora, models, similarities
from rich import print

# —--------------------------------------------

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.INFO)


class LsiModel(object):

    def __init__(self, documents: List[str], num_topics: int) -> None:
        self.documents = documents
        self.num_topics = num_topics
        self._texts = None
        self._dictionary = None
        self._corpus = None
        self._tfidf = None

    @property
    def texts(self) -> List[List[str]]:
        if self._texts is None:
            self._texts = [jieba.lcut(doc) for doc in self.documents]
        return self._texts

    @property
    def corpus(self):
        if self._corpus is None:
            self._corpus = [
                self.dictionary.doc2bow(text) for text in self.texts
            ]
        return self._corpus

    @property
    def dictionary(self):
        if self._dictionary is None:
            self._dictionary = corpora.Dictionary(self.texts)
        return self._dictionary

    def build_model(self):
        self.lsi = models.LsiModel(self.corpus,
                                   id2word=self.dictionary,
                                   num_topics=self.num_topics)
        self.index = similarities.MatrixSimilarity(
            self.lsi[self.corpus])     # 创建索引，用于后续计算相似度
        return self.lsi

    def query(self, query: str, topk:int=100):
        query_bow = self.dictionary.doc2bow(jieba.lcut(query))     # 将查询文档向量化
        query_lsi = self.lsi[query_bow]     # 用之前训练好的lsi模型将其映射到2维topic空间
        sims = self.index[query_lsi]     # 计算query和index中的文档点相似度
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])[:topk]
        texts = [(self.documents[i], _) for i, _ in sort_sims]
        return texts

if __name__=='__main__':
    documents = [k for k in cf.osdb('/tmp/history_articles.db/').keys()]
    documents = cf.io.read('/tmp/t.txt')
    model = LsiModel(documents, 200)
    model.build_model()
    q = '想创建一个基于LLM的聊天机器人，利用你公司的数据？- 加入我的VB转型，了解如何'
    print(model.query(q))
