import ply.lex, argparse, io

# modified from https://gist.github.com/amerberg/a273ca1e579ab573b499

#Usage
# python stripcomments.py input.tex > output.tex
# python stripcomments.py input.tex -e encoding > output.tex

# Modification:
# 1. Preserve "\n" at the end of line comment
# 2. For \makeatletter \makeatother block, Preserve "%" 
#    if it is actually a comment, and trim the line
#    while preserve the "\n" at the end of the line. 
#    That is because remove the % some time will result in
#    compilation failure.

def strip_comments(source):
    tokens = (
                'PERCENT', 'BEGINCOMMENT', 'ENDCOMMENT',
                'BACKSLASH', 'CHAR', 'BEGINVERBATIM',
                'ENDVERBATIM', 'NEWLINE', 'ESCPCT',
                'MAKEATLETTER', 'MAKEATOTHER',
             )
    states = (
                ('makeatblock', 'exclusive'),
                ('makeatlinecomment', 'exclusive'),
                ('linecomment', 'exclusive'),
                ('commentenv', 'exclusive'),
                ('verbatim', 'exclusive')
            )

    # Deal with escaped backslashes, so we don't
    # think they're escaping %
    def t_BACKSLASH(t):
        r"\\\\"
        return t

    # Leaving all % in makeatblock
    def t_MAKEATLETTER(t):
        r"\\makeatletter"
        t.lexer.begin("makeatblock")
        return t

    # One-line comments
    def t_PERCENT(t):
        r"\%"
        t.lexer.begin("linecomment")

    # Escaped percent signs
    def t_ESCPCT(t):
        r"\\\%"
        return t

    # Comment environment, as defined by verbatim package
    def t_BEGINCOMMENT(t):
        r"\\begin\s*{\s*comment\s*}"
        t.lexer.begin("commentenv")

    #Verbatim environment (different treatment of comments within)
    def t_BEGINVERBATIM(t):
        r"\\begin\s*{\s*verbatim\s*}"
        t.lexer.begin("verbatim")
        return t

    #Any other character in initial state we leave alone
    def t_CHAR(t):
        r"."
        return t

    def t_NEWLINE(t):
        r"\n"
        return t

    # End comment environment
    def t_commentenv_ENDCOMMENT(t):
        r"\\end\s*{\s*comment\s*}"
        #Anything after \end{comment} on a line is ignored!
        t.lexer.begin('linecomment')

    # Ignore comments of comment environment
    def t_commentenv_CHAR(t):
        r"."
        pass

    def t_commentenv_NEWLINE(t):
        r"\n"
        pass

    #End of verbatim environment
    def t_verbatim_ENDVERBATIM(t):
        r"\\end\s*{\s*verbatim\s*}"
        t.lexer.begin('INITIAL')
        return t

    #Leave contents of verbatim environment alone
    def t_verbatim_CHAR(t):
        r"."
        return t

    def t_verbatim_NEWLINE(t):
        r"\n"
        return t

    #End a % comment when we get to a new line
    def t_linecomment_ENDCOMMENT(t):
        r"\n"
        t.lexer.begin("INITIAL")

        # Newline at the end of a line comment is presevered.
        return t

    #Ignore anything after a % on a line
    def t_linecomment_CHAR(t):
        r"."
        pass

    def t_makeatblock_MAKEATOTHER(t):
        r"\\makeatother"
        t.lexer.begin('INITIAL')
        return t

    def t_makeatblock_BACKSLASH(t):
        r"\\\\"
        return t

    # Escaped percent signs in makeatblock
    def t_makeatblock_ESCPCT(t):
        r"\\\%"
        return t

    # presever % in makeatblock
    def t_makeatblock_PERCENT(t):
        r"\%"
        t.lexer.begin("makeatlinecomment")
        return t

    def t_makeatlinecomment_NEWLINE(t):
        r"\n"
        t.lexer.begin('makeatblock')
        return t

    # Leave contents of makeatblock alone
    def t_makeatblock_CHAR(t):
        r"."
        return t

    def t_makeatblock_NEWLINE(t):
        r"\n"
        return t

    # For bad characters, we just skip over it
    def t_ANY_error(t):
        t.lexer.skip(1)

    lexer = ply.lex.lex()
    lexer.input(source)
    return u"".join([tok.value for tok in lexer])

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help = 'the file to strip comments from')
    parser.add_argument('--encoding', '-e', default='utf-8')
    
    args = parser.parse_args()
    
    with io.open(args.filename, encoding=args.encoding) as f:
        source = f.read()
    
    print(strip_comments(source))
    
if __name__ == '__main__':
    main()