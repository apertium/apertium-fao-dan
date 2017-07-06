import xml.etree.ElementTree as ET
import re
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()


class Entry:
    def __init__(self, line):
        self.fao_ans = []  # [(lemma, [tags]), ()...]
        self.dan_ans = []
        self.pairs = []

    def get_clear_ans(self):
        def clear_ans(i):  # 0 for Faroese, 1 for Danish
            str_ano = line.strip().split('\t')[i]
            ans = re.findall('/(.*?)/', str_ano)  # ['+Áland<np><sg><acc><guess>', '+Áland<np><sg><nom><guess>', '.<sent>$@^.']
            ans_clear = []  # [(lemma, [tags]), ()...]
            for ana in ans:
                if '<cmp>' not in ana and '<sent>' not in ana and '<punct>' not in ana:
                    lem = re.match('\+?(.*?)\+?<', ana).group(1)
                    tags = tuple()
                    if '<vblex>' in ana:
                        tags = tuple(['<vblex>'])
                    elif '<n>' in ana or '<np>' in ana:
                        tags = tuple(filter(lambda x: x in ana, ['<n>', '<np>', '<m>', '<f>', '<nt>', '<mf>']))
                    elif '<adj>' in ana:
                        tags = tuple(filter(lambda x: x in ana, ['<adj>', '<sint>', '<pos>', '<comp>']))
                    elif '<adv>' in ana:
                        tags = tuple(['<adv>'])
                    ana_clear = tuple([lem, tags])
                    ans_clear.append(ana_clear)
            ans_clear = list(set(ans_clear))
            return ans_clear
        self.fao_ans = clear_ans(0)
        self.dan_ans = clear_ans(1)
        return


# <n> <adj> <adv> <vblex>

    def get_pairs(self):
        pairs = []  # [[fao annotation, dan annotation], []...]
        for fan in self.fao_ans:
            for dan in self.dan_ans:
                if ('<n>' in fan[1] and '<n>' in dan[1]) or ('<adj>' in fan[1] and '<adj>' in dan[1]) or \
                   ('<adv>' in fan[1] and '<adv>' in dan[1]) or ('<vblex>' in fan[1] and '<vblex>' in dan[1]):
                    pairs.append([fan, dan])
        self.pairs = pairs
        return


# ^endaligur/endaligur<adj>$^./.<sent>$@^./.<sent>$	^absolut/absolut<adj><sint>$^./.<sent>$@^./.<sent>$^./.<sent>$
# ---->
# <e><p><l>endaligur<s n="adj"/></l><r>absolut<s n="adj"/><s n="sint"/></r></p></e>
# ^abortera/abortera<vblex><inf>$^./.<sent>$@^./.<sent>$	^abortere/abortere<vblex><inf><actv>$^./.<sent>$@^./.<sent>$^./.<sent>$
# -->
# <e><p><l>abortera<s n="vblex"/></l><r>abortere<s n="vblex"/></r></p></e>
# ^fregna/fregna<vblex><imp><sg>/fregna<vblex><ind><pres><pl>/fregna<vblex><inf>/fregn<n><nt>$^(/(<lquot>/(<punct><left>$^st/styðja<vblex><imp><sg>/st<abbr>$^)/)<punct><right>/)<rquot>$^./.<sent>$@^./.<sent>$	^aflure/aflure<vblex><inf><actv>$^./.<sent>$@^./.<sent>$^./.<sent>$


for line in lines:
    entry = Entry(line)
    entry.get_clear_ans()
    entry.get_pairs()
    for pair in entry.pairs:
        e = ET.Element('e')
        p = ET.SubElement(e, 'p')
        l = ET.SubElement(p, 'l')
        l.text = pair[0][0]
        for tag in pair[0][1]:
            s1 = ET.SubElement(l, 's', n=tag.strip('<>'))
        r = ET.SubElement(p, 'r')
        r.text = pair[1][0]
        for tag in pair[1][1]:
            s2 = ET.SubElement(r, 's', n=tag.strip('<>'))
        ET.dump(e)
