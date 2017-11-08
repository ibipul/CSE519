from project519.docCls import doc_object

class content_preprocessor:
    def __init__(self, doc_object):
        self.doc_object = doc_object


    def remove_math_exp(self):
        """
        This function is used to remove all inline mathematical expressions from the file
        :return:
        """
        return None

    def remove_math_formula(self):
        """
        This function clears out text segments enclosed in $$
        and those enclosed in \begin{equation}\end{equation}
        :return:
        """
        return None

    def clear_math(self):
        """
        Wrapper that initiates math clearing operation on content strings
        :return:
        """
        self.remove_math_exp()
        self.remove_math_formula()

    def clear_comments(self):
        pass

    def clear_latex_keys(self):
        pass

    def preprocess(self):
        # TODO: ibipul@cs.stonybrook.edu
        # Add steps that complete preprocessing
        # Sequentially call above functions
        # Updates sanitized_file_strings of the doc_objects
        return self.doc_object