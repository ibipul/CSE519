### Building Document Index

This project is aimed towards building an automated index creating mechanism.
Component files are:
#### docCls.py
	- Contains the doc_object class definition that encapsulates each complex/simple tex document structure behind a pdf file. *doc_class* is as follows:
    	- tex file names are read into tex_filenames
    	- tex_file_contents contain raw tex file contents read in a string
    	- Extract all index phrases encoded in latex fomats form the text
    	- Preprocess the above to get the english like phrases each line is capturing
    	- memeber variable to contain cleaned file strings (after preprocessing)
    	- memeber variable to contain a set of computer index words on return from evaluation
    	- an evaluation metric per object that quantifies the quality of index generation
