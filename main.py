class trext:
    def __init__(self,p='',s='',newline = True):
        self.prefix = p
        self.suffix = s
        self.content = []
        self.newline = newline
    def __str__(self):
        text = self.prefix
        if self.newline:
            text += '\n'
        text += self.suffix
        return text
    def text(self,n=0):
        text = ''
        # pre
        text += self.prefix
        if self.newline:
            text += '\n'
        # content
        for c in self.content:
            try:
                text += c.text(n=n+1)
            except:
                text += c
                if self.newline:
                    text += '\n'
        # suf
        text += self.suffix
        if self.newline:
            text += '\n'
        return text
    def append(self,c):
        self.content.append(c)
#%% bible data
# Read UTF8 https://stackoverflow.com/a/844443
with open ('bibleData.csv', "r", encoding="utf-8") as myfile:
    data=myfile.readlines()
data = [d.split(',') for d in data]

bible = {}
for row in data:
    verse = int(row[0][-3:])
    chapter = int(row[0][-6:-3])
    book = int(row[0][:-6])
    try:
        bible[book][chapter][verse] = row[1].rstrip()
    except:
        try:
            bible[book][chapter] = {}
        except:
            bible[book] = {}
            bible[book][chapter] = {}
        bible[book][chapter][verse] = row[1].rstrip()
#%% book names
with open ('bookNames.csv', "r", encoding="utf-8") as myfile:
    data = myfile.readlines()
    
data = [d.split(',') for d in data]
names = {}
for row in data:
    names[int(row[2].strip())] = row[0]

#%% latex file
with open ('head.code', "r") as myfile:
    head = myfile.readlines()
head = [h.rstrip() for h in head]
head = '\n'.join(head)

tex = trext(head,'\end{document}')
def chapterTag(b,c=0): 
    out = 'b' + str(b) + 'c' + str(c)
    return out

for book in range(1,67):
    tex.append('\\newpage')
    tex.append('\\section{' + names[book] + '}')
    tex.append('\\hypertarget{' + chapterTag(book) + '}{}')
    tex.append('\\hyperlink{menu}{回目录}\n')
    for chapter in range(1,1+len(bible[book])):
        tex.append('\\hyperlink{' + chapterTag(book,chapter) + '}{[' + str(chapter) + '] }')
    tex.append('\\newpage')
    for chapter in range(1,1+len(bible[book])):
        tex.append('\\hypertarget{' + chapterTag(book,chapter) + '}{}')
        clink = '\\hyperlink{' + chapterTag(book) + '}{\\colorbox{yellow}'
        clink += '{' + names[book] + ' ' + str(chapter) + '}}'
        tex.append(clink)
        for verse in range(1,1+len(bible[book][chapter])):
            tex.append('{\\color{gray}'+str(verse)+'}')
            tex.append(bible[book][chapter][verse])
            if book == 19:
                tex.append('')

import codecs
file = codecs.open("book.tex", "w", "utf-8")
file.write(tex.text())
file.close()

#a = trext('function y = f(x)','end')
#a.append('y = x;')
#a.append('y = y + 1;')
#
#c = trext(p='start')
#c.append(a)
#
#d = trext(p='y = exp(',s=');',newline=False)
#d.append('y')
#a.append(d)
#
#print(d)
#print(a)
#print(c.text())
