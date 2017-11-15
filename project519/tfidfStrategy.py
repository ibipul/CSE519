from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import PorterStemmer
from scipy import stats
import re

class tfidf_model:

    def __init__(self, corpus, lower_threshold, upper_threshold):
        self._LOWER_THRESHOLD = lower_threshold
        self._UPPER_THRESHOLD = upper_threshold
        self.corpus = corpus
        self.stop_words = stopwords.words('english') + list(punctuation)
        self.vocabulary = self.corpus_vocabulary()
        self.model = self.generate_model()
        #self.candidate_word_dict ={}

    def tokenize(self, text):
        stemmer = PorterStemmer()
        words = word_tokenize(text)
        words = [w.lower() for w in words]
        words = [w for w in words if not bool(re.search(r'\d', w))]
        words = [w for w in words if not bool(re.search(r'[%s]'% punctuation, w))]

        stemmed_words =  [stemmer.stem(w) for w in words if w not in self.stop_words and not w.isdigit()]
        return stemmed_words

    def corpus_vocabulary(self):
        vocabulary = set()
        for str in self.corpus:
            words = self.tokenize(str)
            vocabulary.update(words)

        return vocabulary


    def generate_model(self):
        tfidf_obj = TfidfVectorizer(stop_words=self.stop_words,tokenizer=self.tokenize,vocabulary=self.vocabulary)
        return tfidf_obj

    def fit(self,corpus):
        self.model.fit([doc_str for doc_str in corpus])

    def get_dictionary_for_doc(self, document_string):
        X = self.model.transform([document_string])
        doc_tokens = self.tokenize(document_string)

        candidate_word_dict = defaultdict(lambda:0)
        for word in doc_tokens:
            word_score = X[0, self.model.vocabulary_[word]]
            if word_score > 0 :
                candidate_word_dict[word] += word_score
        candidate_word_dict = dict(candidate_word_dict)

        # Get a select subset out of the whole bag based on a quantile score
        final_dict = self.filter_by_threshold(candidate_word_dict=candidate_word_dict,
                                              lower=self._LOWER_THRESHOLD,upper=self._UPPER_THRESHOLD)
        return final_dict

    def filter_by_threshold(self,candidate_word_dict, lower, upper):

        keys = list(candidate_word_dict.keys())
        values = list(candidate_word_dict.values())
        quantile_scores = stats.rankdata(values, 'average') / len(values)

        final_dictionary = defaultdict(lambda:0)
        for i in range(len(quantile_scores)):
            if quantile_scores[i] > lower and quantile_scores[i] < upper:
                key = keys[i]
                value = values[i]
                final_dictionary[key] = value

        return dict(final_dictionary)

    def evaluation_metric_per_truth(self, index_phrases, candidate_word_dict):
        #overlap_count = []
        #index_phrase_count = []
        per_truth_ratio = []
        for text in index_phrases:
            words = self.tokenize(text)
            if len(words) == 0:
                per_truth_ratio.append(0.0)
            else:
                intersect_count = set(words).intersection(set(candidate_word_dict.keys()))
                #overlap_count.append(intersect_count)
                #index_phrase_count.append(len(words))
                per_truth_ratio.append(len(intersect_count)/len(words))

        return sum(per_truth_ratio)/len(index_phrases)

    def evaluation_overlap_ratios(self, index_phrases, candidate_word_dict):
        index_words = []
        for text in index_phrases:
            index_words += self.tokenize(text)

        index_vocabulary = set(index_words)
        overlap = index_vocabulary.intersection(candidate_word_dict.keys())

        index_to_candidates = len(overlap)/len(index_vocabulary)
        candidate_to_index = len(overlap)/len(candidate_word_dict.keys())

        return index_to_candidates, candidate_to_index
