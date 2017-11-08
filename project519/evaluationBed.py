import project519.docCls
from project519.docClean import content_preprocessor

class evaluation_bed:
    def __init__(self, doc_obj_list):
        self.doc_objs = doc_obj_list
        self.preprocessed_doc_objects = []

    def preprocessing(self):
        for obj in self.doc_objs:
            doc_preprocessor = content_preprocessor(doc_object=obj)
            preprocessed_obj = doc_preprocessor.preprocess()
            self.preprocessed_doc_objects.append(preprocessed_obj)

    # Define performance metric
    def evaluation_metric(self, doc_obj):
        pass

    # Define index computation algorithm
    def plugin_algorithm(self, algorithm_object):
        pass

    # Update each doc object with performance metric
    def per_object_evaluation(self):
        pass