import re
import shutil
import tempfile
import zipfile
import os
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
    if 1 <= len(word) and len(word) > 5:
        if word[0] in letters and not (word.lower() in WORD_DICT or word.lower().rstrip("s") in WORD_DICT):
            for x in xrange(1,len(word)):
                p1 = word[:x]
                p2 = word[x:]
##                print p1,p2
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

def remove_from_zip(zipfname, out_zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        zipread = zipfile.ZipFile(zipfname, 'r')
        zipwrite = zipfile.ZipFile(tempname, 'w')
        for item in zipread.infolist():
            if item.filename not in filenames:
                data = zipread.read(item.filename)
                zipwrite.writestr(item, data)
        zipread.close()
        zipwrite.close()
        shutil.move(tempname, out_zipfname)
    finally:
        shutil.rmtree(tempdir)

regex_get_blocks = re.compile("(<.*?>)")
regex_get_words = re.compile("([^a-zA-Z]*)")
WORD_DICT = set(load_words('words.txt'))

root = Tkinter.Tk()
root.withdraw()
in_zip_path = tkFileDialog.askopenfilename(title="Open Text")
out_zip_path = tkFileDialog.asksaveasfilename(title="Save Text")

zipy = zipfile.ZipFile(in_zip_path,"r")

regex = re.compile(r"calibre.*?[/].*?[.]html")

for name in zipy.namelist():
    if re.match(regex,name):
        break

fileinfo = zipy.getinfo(name)
f = zipy.open(name,"r")
data = f.read()
f.close()
zipy.close()


cleaned_book = clean_book(data)

remove_from_zip(in_zip_path,out_zip_path,name)

zipy = zipfile.ZipFile(out_zip_path,"a")
zipy.writestr(fileinfo,cleaned_book)
zipy.close()

##root.quit()
raw_input("Press enter to quit")
