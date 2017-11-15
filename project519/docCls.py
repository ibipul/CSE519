import glob
import re
import io
from collections import defaultdict

class doc_object:
    """
    doc_object is the class that encapsulates each complex/simple tex document structure
    behind a pdf file.
    1. tex file names are read into tex_filenames
    2. tex_file_contents contain raw tex file contents read in a string
    """
    def __init__(self, dir_path):
        """
        Constructor for doc_object class
        :param dir_path string: base folder of each directory containing the tex files
        """
        self.dir_path = dir_path
        self.dirname = self.dir_path.split('\\')[-2]
        self.tex_filenames = self.read_filenames(doc_directory=self.dir_path)
        ## File content related variables
        self.tex_file_contents = self.read_files_as_string(filenames_list=self.tex_filenames)
        self.sanitized_file_strings = []  # Updated by preprocessor
        self.doc_string = ''

        # Index related Variables
        self.index_ground_truth = self.extract_index_words(content_strings=self.tex_file_contents)
        self.index_keywords = self.raw_keywords(ground_truth=self.index_ground_truth)
        self.computed_index_words = [] # Updated by evaluation bed TODO ibipul

        ## Evaluation Metrics
        self.evaluation_performance_per_index = []
        self.evaluation_index_to_candidates = 0.0
        self.evaluation_candidates_to_index = 0.0

    def read_filenames(self, doc_directory):
        """
        Function to read all tex file names in the base directory
        :param doc_directory string:
        :return filenames list:
        """
        tex_files = glob.glob(doc_directory + '*.tex')
        return tex_files

    def read_files_as_string(self, filenames_list):
        """
        Reads Contents of tex files
        :param filenames_list list[char]: list of component filenames
        :return: list of contents of files as strings
        :rtype list[char]:
        """
        content_strings = []
        for file_name in filenames_list:
            with io.open(file_name, encoding='latin-1') as content_file:
                content = content_file.read()
                content_strings.append(content)
        return content_strings

    def extract_index_words(self, content_strings):
        """
        Extracts and returns a list of index words encoded in the tex files
        :return: a list of index words extracted
        :rtype list[char]
        """
        p = re.compile(r'index\{([\w|\s|\{|\}|\||\!|\-|\\|\']+)\}', re.I)

        index_word_list = []
        for cont_str in content_strings:
            list_from_a_string = p.findall(cont_str)
            index_word_list += list_from_a_string

        sanitized_list = []
        p1 = re.compile(r'([\s|\w|\W]+)\}(?:[\s|\W|begin|end]+)\{[\s|\w|\W]+',re.I)
        for word in index_word_list:
            if "}\\index{" in word:
                w_splits = word.split("}\\index{")
                sanitized_list += w_splits
            elif "\\begin" in word:
                shortened_word = p1.findall(word)
                sanitized_list += shortened_word
            elif "\\end" in word:
                shortened_word = p1.findall(word)
                sanitized_list += shortened_word
            else:
                sanitized_list.append(word)

        return sanitized_list

    def raw_keywords(self,ground_truth):
        keyword_list = []
        for word in ground_truth:
            if '|' in word:
                w_split = word.split('|')
                if '!' in w_split[0]:
                    tword = w_split[0].replace('!',' ')
                    keyword_list.append(tword)
                else:
                    keyword_list.append(w_split[0])
            elif '!' in word:
                tword = word.replace('!', ' ')
                keyword_list.append(tword)
            else:
                keyword_list.append(word)

        return keyword_list