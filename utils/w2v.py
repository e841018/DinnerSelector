import jieba
import json
import re
import glob
import os
import word2vec

class CorpusGenerator():
    def __init__(self, review_folder='../data/reviews_by_guide/'):
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
                new_terms.remove(t)
        return new_terms

    def get_review_content(self, filename):
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
    
    def gen(self):
        """ Save corpus to file """
        with open('../data/corpus.txt', 'w') as f:
            for fn in self.filenames:
                # [['第一', '間', '店', '的', '評論'], ['第二', '間', '店', '的', '評論'], ...]
                reviews_terms = self.get_review_content(fn)

                for terms in reviews_terms:
                    f.write(' '.join(terms) + '\n')

if __name__ == "__main__":
    # generate corpus
    corpus_gen = CorpusGenerator()
    corpus_gen.gen()

    # word2vec model
    word2vec.word2vec('../data/corpus.txt',
        '../model/corpusWord2Vec.bin', size=300, min_count=3, verbose=True)
    model = word2vec.load('../model/corpusWord2Vec.bin')

    indices, metrices = model.similar(u'飲料')
    for index, mt in zip(indices, metrices):
        print(model.vocab[index], mt)
