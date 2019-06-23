import jieba
import json
import re
import glob
import os
import numpy as np
from gensim.models import word2vec
import logging

class CorpusGenerator():
    def __init__(self, guide_review_folder='../data/reviews_guide/', place_review_folder='../data/reviews_place'):
        self.EMOJI_RE = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u2B55'
            u'\u23cf'
            u'\u23e9'
            u'\u231a'
            u'\u3030'
            u'\ufe0f'
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u'\U00010000-\U0010ffff'
            u'\U0001F1E0-\U0001F1FF'  # flags (iOS)
            u'\U00002702-\U000027B0]+', re.UNICODE)

        self._init_jieba()
        self.filenames = glob.glob(os.path.join(guide_review_folder, '*.json')) + glob.glob(os.path.join(place_review_folder, '*.json'))
        self.stopwords = set()

        with open('../data/stopWords.txt', 'r', encoding='UTF-8') as file:
            for data in file.readlines():
                self.stopwords.add(data.strip())

    def _init_jieba(self):
        # set traditional chinese-friendly dictionary
        jieba.set_dictionary('../data/jieba_dict/dict.txt.big')

    def clean(self, content):
        # remove non-Chinese, non-Engilsh and emoji
        content = re.sub(u'[^\u4e00-\u9fff^\w]', '', content)
        return self.EMOJI_RE.sub('', content)

    def remove_stop_words(self, terms):
        terms_copy = [t for t in terms]
        for t in terms_copy:
            if t in self.stopwords:
                terms.remove(t)
            if len(t) > 20:
                terms.remove(t)

    def get_review_content(self, filename):
        with open(filename, 'r') as f:
            pkg = json.load(f)

        reviews_terms = []
        for review in pkg:
            content = self.clean(review['content'])
            terms = list(jieba.cut(content))
            self.remove_stop_words(terms)

            # > 1 to filter english
            if len(terms) > 1:
                reviews_terms.append(terms)
        return reviews_terms

    def get_placeReview_content(self, filename):
        with open(filename, 'r') as f:
            pkg = json.load(f)

        reviews_terms = []
        reviews_origin = []
        for review in pkg:
            content = self.clean(review['content'])
            terms = list(jieba.cut(content))
            self.remove_stop_words(terms)

            if len(terms) > 0:
                reviews_terms.append(terms)
                reviews_origin.append(review['content'])
        return reviews_terms,reviews_origin
    
    def gen(self, corpus_path='../data/corpus.txt'):
        """ Save corpus to file """
        with open(corpus_path, 'w') as f:
            for fn in self.filenames:
                # [['第一', '間', '店', '的', '評論'], ['第二', '間', '店', '的', '評論'], ...]
                reviews_terms = self.get_review_content(fn)

                for terms in reviews_terms:
                    f.write(' '.join(terms) + '\n')
class Word2Vec():
    """
        @gen_corpus: Generate new corpus from dataset in `data_folder`
        @train: Training a new word2vec model
    """
    def __init__(self, gen_corpus=False, train=False, model_name=None, vec_dim=100, min_count=3):
        # generate corpus file
        if gen_corpus:
            self.cg = CorpusGenerator()
            self.cg.gen(corpus_path='../data/corpus.txt')

        # Train a model to generate embedding(vector) for each vocab
        # A vocab is a word that appears > min_count times in the corpus
        if train:
            logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
            sentences = word2vec.LineSentence('../data/corpus.txt')
            model = word2vec.Word2Vec(sentences, sg=1, size=vec_dim, min_count=min_count)
            model.save('../model/w2v_{}.model'.format(vec_dim))    
            self.model = word2vec.Word2Vec.load('../model/w2v_{}.model'.format(vec_dim))
        else:
            assert model_name != None
            self.model = word2vec.Word2Vec.load(model_name)


    def get_relevant_words(self, query_word, topn=10):
        return self.model.most_similar(query_word, topn=topn)

    def get_word_vector(self, query_word):
        try:
            return self.model[query_word]
        except KeyError:
            print('[KeyError] Can\'t recognize the query word')
            return None

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store_true', dest='train', default=False)
    parser.add_argument('-g', action='store_true', dest='gen', default=False)
    parser.add_argument('-p', action='store', dest='corpus_p', default='../data/corpus.txt')
    parser.add_argument('--model_name', action='store', dest='model_name', default='../model/w2v_dim-100.model')
    args = parser.parse_args()

    # sample code to get similar words
    w2v = Word2Vec(gen_corpus=args.gen, train=args.train, model_name=args.model_name)
    keywords = ['舒服', '衛生', '飲料', '服務', '便宜', '冷氣']
    for kwd in keywords:
        print('Keywords: {}'.format(kwd))
        results = w2v.get_relevant_words(kwd, 10)
        for w, mt in results:
            print(w, mt)
        print('------------------')
