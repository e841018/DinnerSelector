import jieba
import json
import re
import glob
import os
import numpy as np
from gensim.models import word2vec
import logging

class CorpusGenerator():
    def __init__(self, review_folder='../data/reviews_guide/'):
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
        self.filenames = glob.glob(os.path.join(review_folder, '*.json'))
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
        new_terms = [t for t in terms]
        for t in terms:
            if t in self.stopwords:
                terms.remove(t)
        #return new_terms

    def get_review_content(self, filename):
        with open(filename, 'r') as f:
            pkg = json.load(f)

        reviews_terms = []
        reviews_places = []
        for review in pkg:
            content = self.clean(review['content'])
            place = review['place']
            terms = list(jieba.cut(content))
            self.remove_stop_words(terms)

            if len(terms) > 1:
                reviews_terms.append(terms)
                reviews_places.append(place)
        return reviews_terms, reviews_places

    def get_placeReview_content(self, filename):
        with open(filename, 'r') as f:
            pkg = json.load(f)

        reviews_terms = []
        for review in pkg:
            content = self.clean(review['content'])
            terms = list(jieba.cut(content))
            terms = self.remove_stop_words(terms)

            if len(terms) > 0:
                reviews_terms.append(terms)
        return reviews_terms


    def gen(self, corpus_path='../data/corpus.txt'):
        """ Save corpus to file """
        with open(corpus_path, 'w') as f:
            for fn in self.filenames:
                # [['第一', '間', '店', '的', '評論'], ['第二', '間', '店', '的', '評論'], ...]
                reviews_terms, _ = self.get_review_content(fn)

                for terms in reviews_terms:
                    f.write(' '.join(terms) + '\n')
class Word2Vec():
    """
        @gen_corpus: Generate new corpus from dataset in `data_folder`
        @train: Training a new word2vec model
    """
    def __init__(self, gen_corpus=False, train=False, corpus_path='../data/corpus.txt',
            data_folder='../data/reviews_guide/', vec_dim=300, min_count=3):
        # generate corpus file
        if gen_corpus:
            self.cg = CorpusGenerator(review_folder=data_folder)
            self.cg.gen(corpus_path=corpus_path)

        # Train a model to generate embedding(vector) for each vocab
        # A vocab is a word that appears > min_count times in the corpus
        if train:
            logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
            sentences = word2vec.LineSentence(corpus_path)
            model = word2vec.Word2Vec(sentences, sg=1, size=vec_dim, min_count=min_count)
            model.save('../model/w2v_wiki.model')    
            
            # word2vec.word2vec(corpus_path,
            #     '../model/corpusWord2Vec.bin', size=vec_dim, min_count=min_count, verbose=True)
        
        self.model = word2vec.Word2Vec.load('../model/w2v_wiki.model')
        # self.model = word2vec.load('../model/corpusWord2Vec.bin')

    def get_relevant_words(self, query_word):
        return self.model.most_similar(query_word)

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
    args = parser.parse_args()


    # sample code to get similar words
    w2v = Word2Vec(gen_corpus=args.gen, train=args.train, corpus_path=args.corpus_p, vec_dim=250)
    words, metrices = w2v.get_relevant_words(u'火鍋')
    print('\n')
    for w, mt in zip(words, metrices):
        print(w, mt)

    # sample code to acquire word embedding
    drinks_vec = w2v.get_word_vector(u'飲料')
    print('飲料\'s vector dim1~10: ', drinks_vec[:10])
