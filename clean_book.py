import re
import Tkinter, tkFileDialog

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
    if 3 <= len(word)-2:
        if not (word.lower() in WORD_DICT):
            for x in range(3,len(word)-2):
                p1 = word[:x]
                p2 = word[x:]
                if p1.lower() in WORD_DICT and p2.lower() in WORD_DICT:
                    if p2[0].lower() == "s" and p2[1:].lower() in WORD_DICT:
                        p1+=p2[0]
                        p2 = p2[1:]
                    return p1+" "+p2

def clean_book(data):
    words = re.split(regex_get_words,data)

    corrections = 0
    for word in range(len(words)):
        comp = compound(words[word])
        if comp:
            print str(corrections)+" - "+words[word]+" ==> "+comp
            words[word] = comp
            corrections += 1
            
    out = "".join(words)
    print "Compleate with %d corrections"%corrections
    return out


regex_get_words = re.compile("([^a-zA-Z]*)")
WORD_DICT = load_words('words.txt')

root = Tkinter.Tk()
root.withdraw()
f = tkFileDialog.askopenfile(title="Open Text")
data = f.read()
f.close()
f = tkFileDialog.asksaveasfile(mode="w",title="Save Text")
f.write(clean_book(data))
f.close()
root.quit()

