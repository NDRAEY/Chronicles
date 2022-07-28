TOKENLIST = "(){}[],.:;*+-/@#$\"\' =^~|%<>\n";

def tokenize(code):
    tokens = []
    sptokens = []
    for i in code:
        if i in TOKENLIST:
            if len(sptokens):
                tokens.append(''.join(sptokens))
                sptokens = []
            tokens.append(i)
        else:
            sptokens.append(i)

    if len(sptokens):
        tokens.append(''.join(sptokens))
        sptokens = []
    return tokens

if __name__=="__main__":
    print(tokenize("72+11*7-4/2+19+95"))
