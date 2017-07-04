import xml.etree.ElementTree as ET
import re
import sys

dct = ET.parse(sys.argv[1])
root = dct.getroot()


class Entry:
    def __init__(self, gr):
        self.dan = gr[2][0].text
        self.faos = []
        ms = gr.findall('.//M')
        if ms and ms[0].text and not re.match('\W+$', ms[0].text):
            self.faos = ms[0].text.replace(';', ',').split(',')
        self.faos = [fao.strip() for fao in self.faos]
        self.comment = ''
        c = gr.findall('.//K')
        if c:
            self.comment = c[0].text


for i in range(len(root)):
    entry = Entry(root[i])
    for fao in entry.faos:
        print(':'.join((fao, entry.dan)))


"""
brackets = {}
for i in range(len(root)):
    entry = Entry(root[i])
    for fao in entry.faos:
        m = re.match('.*?\((.*?)\).*?', fao)
        if m:
            if m.group(1) not in brackets:
                brackets[m.group(1)] = []
            brackets[m.group(1)].append(fao)

for b in brackets:
    if len(brackets[b]) != 1:
        print(b)
        print('=====')
        for fao in brackets[b]:
            print(fao)
        print('')
"""