from glob import glob
from project519.docCls import doc_object
from project519.evaluationBed import evaluation_bed
_TEST_ROOT = 'C:\\Users\\ibipul\\codes\\datasets\\arxiv\\'
_LATEX_DIRS = glob(_TEST_ROOT+"/*/")

# dlist = [tobj]
# eb = evaluation_bed(dlist)
# eb.plugin_algorithm('tfidf',0,1)

def main():
    dlist = [doc_object(dir_path) for dir_path in _LATEX_DIRS]
    eval_environment = evaluation_bed(doc_obj_list=dlist)
    eval_environment.plugin_algorithm(algorithm_name='tfidf', lower=0.40, upper=0.95)

    for obj in dlist:
        print(
            "Dirname: '{0}', index_capture: '{1}', Overlap/True Index words:'{2}',Overlap/Candidate words: '{3}'".format(
            obj.dirname, round(obj.evaluation_performance_per_index, 3), round(obj.evaluation_index_to_candidates, 3),
            round(obj.evaluation_candidates_to_index, 3)))

# print(" Index Truth capture Ratio: ", doc.evaluation_performance_per_index)
# print(" Overlap words/ True Index words:", doc.evaluation_index_to_candidates)
# print(" Overlap words/ Candidate word set:", doc.evaluation_candidates_to_index)
if __name__ == "__main__":
    main()
