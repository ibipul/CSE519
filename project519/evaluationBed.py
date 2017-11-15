from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import PorterStemmer
import re

from project519.docCls import doc_object
from project519.docClean import content_preprocessor
from project519.tfidfStrategy import tfidf_model

class evaluation_bed:
    def __init__(self, doc_obj_list):
        self.doc_objs = doc_obj_list
        self.preprocessed_doc_objects = self.preprocessing()
        self.corpus = self.get_corpus()
        self.model = None


    def preprocessing(self):
        preprocessed_obj_list = []
        for obj in self.doc_objs:
            doc_preprocessor = content_preprocessor(doc_object=obj)
            preprocessed_obj = doc_preprocessor.preprocess()
            preprocessed_obj_list.append(preprocessed_obj)

        return preprocessed_obj_list

    def get_corpus(self):
        docs = []
        for doc_obj in self.preprocessed_doc_objects:
            docs.append(doc_obj.doc_string)

        return docs

    # Define index computation algorithm
    def plugin_algorithm(self, algorithm_name='tfidf',lower = 0, upper = .99):
        if algorithm_name == 'tfidf':
            tfidf_obj = tfidf_model(corpus=self.corpus, lower_threshold=lower, upper_threshold=upper)
            tfidf_obj.fit(self.corpus)
            self.model = tfidf_obj
            for doc in self.doc_objs:
                candidate_words_dict = tfidf_obj.get_dictionary_for_doc(doc.doc_string)
                doc.candidate_words_dict = candidate_words_dict
                self.per_object_evaluation(doc=doc)
                print(" Index Truth capture Ratio: ", doc.evaluation_performance_per_index)
                print(" Overlap words/ True Index words:", doc.evaluation_index_to_candidates)
                print(" Overlap words/ Candidate word set:", doc.evaluation_candidates_to_index)
        else:
            raise ValueError('That Algorithm is Not implemented yet')

    # Update each doc object with performance metric
    def per_object_evaluation(self, doc):
        doc.evaluation_performance_per_index = \
            self.model.evaluation_metric_per_truth(index_phrases=doc.index_keywords,
                                                   candidate_word_dict=doc.candidate_words_dict)
        doc.evaluation_index_to_candidates, doc.evaluation_candidates_to_index = \
            self.model.evaluation_overlap_ratios(index_phrases=doc.index_keywords,
                                                 candidate_word_dict=doc.candidate_words_dict)
