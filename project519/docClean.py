import re
from project519.docCls import doc_object
from project519.strip_comments import strip_comments
class content_preprocessor:
    def __init__(self, doc_object):
        """
         content_preprocessor constructor
        :param doc_object doc_object:
        """
        self.doc_object = doc_object

    def remove_math_exp(self):
        """
        This function is used to remove all inline mathematical expressions from the file
        """
        p = re.compile(r'\$([^\$]+)\$+', re.I)
        content_string_list = self.doc_object.sanitized_file_strings
        math_exp_sanitized_string_list = []
        for cont_str in content_string_list:
            math_exp_sanitized_string = re.sub(p, '', cont_str)
            math_exp_sanitized_string_list.append(math_exp_sanitized_string)

        self.doc_object.sanitized_file_strings = math_exp_sanitized_string_list

    def remove_math_formula(self):
        """
        This function clears out text segments enclosed in $$
        and those enclosed in \begin{equation}\end{equation}
        :return:
        """
        pass

    def clear_math(self):
        """
        Wrapper that initiates math clearing operation on content strings
        :return:
        """
        self.remove_math_exp()
        self.remove_math_formula()

    def clear_comments(self):
        """
        Calls dzhuang/strip_comments.py for comment removal
        Default encoding is now set to latin-1 other option is utf-8
        """
        content_string_list = self.doc_object.tex_file_contents
        comment_removed_content_list = []
        for cont_str in content_string_list:
            comment_removed_content = strip_comments(cont_str)
            comment_removed_content_list.append(comment_removed_content)

        self.doc_object.sanitized_file_strings = comment_removed_content_list

    def sanitize_whitespace(self):
        """
        Clears substansive extra formatting white spaces in the text
        """
        content_string_list = self.doc_object.sanitized_file_strings
        space_sanitized_string_list = []
        for cont_str in content_string_list:
            space_sanitized_string = re.sub('\s+',' ', cont_str)
            space_sanitized_string_list.append(space_sanitized_string)

        self.doc_object.sanitized_file_strings = space_sanitized_string_list

    def clear_latex_keys(self):
        pass

    def preprocess(self):
        """
        Invocation creates sanitized file strings of latex files for index computation
        component functions are sequentially called
        :return: doc_object with sanitized filestrings updated
        :rtype doc_object:
        """
        # TODO: ibipul@cs.stonybrook.edu

        self.clear_comments()
        self.sanitize_whitespace()
        self.clear_math()
        self.doc_object.doc_string = ''.join(self.doc_object.sanitized_file_strings)
        return self.doc_object