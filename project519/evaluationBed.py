from project519.docCls import doc_object
from project519.docClean import content_preprocessor
from project519.tfidfStrategy import tfidf_model

#_LATEX_BLACK_LIST_PACKAGE_NAME = "C:\\Users\\ibipul\\codes\\CSE519-2017-111578726\\project519\\some_frequent_latex_packages.txt"
class evaluation_bed:
    def __init__(self, doc_obj_list):
        self.doc_objs = doc_obj_list
        #self.pkg_blacklist = self.read_latex_blacklist_pkg()
        self.preprocessed_doc_objects = self.preprocessing()
        self.corpus = self.get_corpus()
        self.model = None


    # def read_latex_blacklist_pkg(self,file= _LATEX_BLACK_LIST_PACKAGE_NAME):
    #     with open(file) as f:
    #         blist = f.read().splitlines()
    #     return blist

    # def remove_blacklisted_package_ocurrence(self, cstr):
    #     return ' '.join([i for i in cstr.split() if i not in self.pkg_blacklist])

    def preprocessing(self):
        preprocessed_obj_list = []
        for obj in self.doc_objs:
            if len(obj.index_keywords) == 0:
                print("Directory: ", obj.dirname, " has a deeper hierarchy. Skipping")
                continue
            doc_preprocessor = content_preprocessor(doc_object=obj)
            preprocessed_obj = doc_preprocessor.preprocess()
            print(preprocessed_obj.dirname)
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
            print(" Creating the TF.IDF model from sklearn")
            print(" Using ", len(self.preprocessed_doc_objects)," documents, these are fine")
            tfidf_obj = tfidf_model(corpus=self.corpus, lower_threshold=lower, upper_threshold=upper)
            print(" Fitting the Corpus to the model")
            tfidf_obj.fit()
            self.model = tfidf_obj
            print("Running update on each doc based on TFIDF we have defined")
            for doc in self.preprocessed_doc_objects:
                print("Executing for doc in: ", doc.dirname)
                candidate_words_dict = tfidf_obj.get_dictionary_for_doc(doc.doc_string)
                doc.candidate_words_dict = candidate_words_dict
                self.per_object_evaluation(doc=doc)

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
