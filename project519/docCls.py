import glob
class doc_object:
    def __init__(self, dir_path):
        self.tex_filenames = self.read_filenames(doc_directory=dir_path)
        self.text_file_contents = self.read_files_as_string(filenames_list=self.tex_filenames)

    def read_filenames(self,doc_directory):
        tex_files = glob.glob(doc_directory + '\\*.tex')
        return tex_files

    def read_files_as_string(self, filenames_list):
        content_strings = []
        for file_name in filenames_list:
            with open(file_name, 'r') as content_file:
                content = content_file.read()
                content_strings.append(content)
        return content_strings



