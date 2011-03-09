import re
import Tkinter, tkFileDialog

letters = "abcdefghijklmnopqrstuvwxyz"

def load_words(filename):
    words = []
    f = open(filename)
    for word in f:
        word = word.strip()
        if word:
            words.append(word.lower())
    f.close()
    return words

def compound(word):
    if 2 <= len(word)-1:
        if word[0] in letters and not (word.lower() in WORD_DICT or word.lower().rstrip("s") in WORD_DICT):
            for x in xrange(1,len(word)-1):
                p1 = word[:x]
                p2 = word[x:]
                if len(p1) + len(p2) != 6:
                    if p1.lower() in WORD_DICT and p2.lower() in WORD_DICT:
                        if p2[0].lower() == "s" and p2[1:].lower() in WORD_DICT:
                            p1+=p2[0]
                            p2 = p2[1:]
                        return p1+" "+p2

def clean_book(data):
    corrections = 0
    print "Starting"
    blocks = re.split(regex_get_blocks,data)
    print "Blocks identified"
    clean_blocks = []
    for block in blocks:
        if block:
            if block[0] == "<":
                clean_blocks.append(block)
            else:
                clean, count = clean_text(block,corrections)
                corrections=count
                clean_blocks.append(clean)
    print "Compleate with %d corrections"%corrections
    return "".join(clean_blocks)
            
def clean_text(data,corrections=0):
    words = re.split(regex_get_words,data)
##    print "Blobs identified"

    for word in range(len(words)):
        comp = compound(words[word])
        if comp:
            print str(corrections)+" - "+words[word]+" ==> "+comp
            words[word] = comp
            corrections += 1
    out = "".join(words)
    return out,corrections


regex_get_blocks = re.compile("(<.*?>)")
regex_get_words = re.compile("([^a-zA-Z]*)")
##regex_get_words = re.compile("((?:[^a-zA-Z])*|(?:<.*?>))")#
WORD_DICT = set(load_words('words.txt'))

root = Tkinter.Tk()
root.withdraw()
f = tkFileDialog.askopenfile(mode="rb",title="Open Text")
data = f.read()
f.close()
f = tkFileDialog.asksaveasfile(mode="w",title="Save Text")
f.write(clean_book(data))
f.close()
##root.quit()
raw_input("Press enter to quit")
