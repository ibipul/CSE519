from collections import defaultdict
from string import punctuation
from nltk import word_tokenize
from nltk import PorterStemmer
from scipy import stats
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import pos_tag
from gensim import corpora
import gensim

class lda_model:

    #Class Tokenizer & Stop words
    _TOKENIZER = RegexpTokenizer(r'\w+')
    _EN_STOP_WORDS = set(stopwords.words('english'))
    _FILTER_POS_LIST = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',
                      'WP', 'WDT', 'RB', 'MD', 'RBR', 'RBS', 'PRP', 'JJ', 'JJR', 'JJS', 'IN', 'DT', 'CD', 'CC']

    def __init__(self, doc_string, num_topics, num_words):
        self._NTOPICS = num_topics
        self._NWORDS = num_words
        self.doc_string = doc_string
        self.model = self.generate_model()
        self.index_words = self.get_index_words()
        #self.candidate_word_dict ={}

    def filter_black_list(self, tok_list):
        """
        Makes sure we filter out most forms of parts of speech
        from our index words
        :param tok_list:
        :return:
        """
        white_list_words = []
        remove_pos = self._FILTER_POS_LIST
        for tok in tok_list:
            if tok[1] not in remove_pos:
                white_list_words.append(tok[0])
        return white_list_words

    def process_doc(self):
        texts = []
        raw = self.doc_string.lower()
        tokens = self._TOKENIZER.tokenize(raw)
        # tok_pos_tagged = pos_tag(tokens)
        # tok_white = filter_black_list(tok_pos_tagged)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in self._EN_STOP_WORDS]
        # stem tokens
        # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to list
        texts.append(stopped_tokens)
        dictionary = corpora.Dictionary(texts)
        # convert tokenized documents into a document-term matrix
        corp = [dictionary.doc2bow(text) for text in texts]
        ## Return the doc term matrix
        return corp, dictionary

    def generate_model(self):
        doc_term_mat, dictionary = self.process_doc()
        lda_obj = gensim.models.ldamodel.LdaModel(doc_term_mat, num_topics=self._NTOPICS, id2word=dictionary, passes=5)
        return lda_obj

    def get_index_words(self):
        nwords = self._NWORDS/self._NTOPICS
        results = self.model.print_topics(num_topics=self._NTOPICS, num_words=nwords)
        ilist = []
        for i in results:
            l = [x.split('*')[1] for x in i[1].replace('"', '').split('+')]
            ilist += l
        return ilist
