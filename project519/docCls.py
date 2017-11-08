import glob
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
        self.tex_filenames = self.read_filenames(doc_directory=dir_path)
        self.tex_file_contents = self.read_files_as_string(filenames_list=self.tex_filenames)

        self.index_ground_truth = self.extract_index_words(content_strings=self.tex_file_contents)
        self.sanitized_file_strings = [] # TODO:ibipul@cs.stonybrook.edu
        self.compted_index_words = [] # TODO:ibipul@cs.stonybrook.edu
        self.evaluation_performance = 0.0 # TODO:ibipul@cs.stonybrook.edu

    def read_filenames(self, doc_directory):
        """
        Function to read all tex file names in the base directory
        :param doc_directory string:
        :return filenames list:
        """
        tex_files = glob.glob(doc_directory + '\\*.tex')
        return tex_files

    def read_files_as_string(self, filenames_list):
        content_strings = []
        for file_name in filenames_list:
            with open(file_name, 'r') as content_file:
                content = content_file.read()
                content_strings.append(content)
        return content_strings



    def extract_index_words(self, content_strings):
        """
        Extracts and returns a list of index words encoded in the tex files
        :return:
        """
        return []




