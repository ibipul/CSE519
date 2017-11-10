from project519.docCls import doc_object
from project519.docClean import content_preprocessor
TEST_PATH = 'C:\\Users\\ibipul\\codes\\datasets\\arxiv\\1111'
tobj = doc_object(dir_path=TEST_PATH)
c = content_preprocessor(tobj)

# l = [... dirpath1, dirpath2,...]
# x= []
# for f in l:
#     obj = doc_object(dir_path=f)
#     x.append(obj)
def main():
    # test_obj = doc_object(dir_path=TEST_PATH)
    # c = content_preprocessor(test_obj)
    #
    # text_file = open("Output.txt", "w")
    # text_file.write(x.sanitized_file_strings)
    # text_file.close()
    pass
if __name__ == "__main__":
    main()
