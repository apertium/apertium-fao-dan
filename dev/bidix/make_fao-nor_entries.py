import xml.etree.ElementTree as ET
import sys
from html import unescape

# python3 make_fao-nor_entries.py fao-dan apertium-dan-nor.dan-nor.dix intersection


def find_intersect(fd, dn):

    n_dan_entries = []
    dan_nor = ET.fromstring(dn)[3]
    for child in dan_nor:
        try:
            n_dan_lemma = child[0][0].text
            n_dan_pos = ''
            if len(child[0][0]) > 0 and 'n' in child[0][0][0].attrib.keys():
                n_dan_pos = child[0][0][0].attrib['n']
            n_dan_entry = tuple([n_dan_lemma, n_dan_pos])
            n_dan_entries.append(n_dan_entry)
        except IndexError:
            pass

    f_dan_entries = []
    for line in fd:
        entry = ET.fromstring(line)
        f_dan_lemma = entry[0][1].text
        f_dan_pos = ''
        if len(entry[0][0]) > 0 and 'n' in entry[0][0][0].attrib.keys():
            f_dan_pos = entry[0][0][0].attrib['n']
        f_dan_entry = tuple([f_dan_lemma, f_dan_pos])
        f_dan_entries.append(f_dan_entry)
    inter = set(n_dan_entries).intersection(set(f_dan_entries))

    for nde in n_dan_entries:
        try:
            if len(nde[1]) == 0 and nde[0] in [fde[0] for fde in f_dan_entries]:
                inter.add(nde)
        except IndexError:
            print('ACHTUNG', nde)

    return inter


def make_entries(pair, fd, dn):  # (danish word, pos)

    dan_nor = ET.fromstring(dn)[3]
    for child in dan_nor:
        try:
            n_dan_lemma = child[0][0].text
            n_dan_pos = ''
            if len(child[0][0]) > 0 and 'n' in child[0][0][0].attrib.keys():
                n_dan_pos = child[0][0][0].attrib['n']
            if n_dan_lemma == pair[0] and (n_dan_pos == pair[1] or len(pair[1]) == 0):
                nor_lemma = child[0][1].text
                nor_tags = []
                if len(child[0][1]) > 0:
                    for tag in child[0][1]:
                        nor_tags.append(tag.attrib['n'])
                nor_vr = ''
                if 'vr' in child.attrib.keys():
                    nor_vr = child.attrib['vr']
                break
        except IndexError:
            pass

    for line in fd:
        entry = ET.fromstring(line)
        f_dan_lemma = entry[0][1].text
        f_dan_pos = ''
        if len(entry[0][0]) > 0 and 'n' in entry[0][0][0].attrib.keys():
            f_dan_pos = entry[0][0][0].attrib['n']
        if f_dan_lemma == pair[0] and (f_dan_pos == pair[1] or len(pair[1]) == 0):
            fao_lemma = entry[0][0].text
            fao_tags = []
            if len(entry[0][1]) > 0:
                for tag in entry[0][1]:
                    fao_tags.append(tag.attrib['n'])
            break

    return tuple([nor_vr, fao_lemma, fao_tags, nor_lemma, nor_tags])


def make_xml(raw):
    e = ET.Element('e')
    if len(raw[0]) > 0:
        e.attrib['vr'] = raw[0]
    p = ET.SubElement(e, 'p')
    l = ET.SubElement(p, 'l')
    l.text = raw[1]
    for tag in raw[2]:
        s1 = ET.SubElement(l, 's', n=tag)
    r = ET.SubElement(p, 'r')
    r.text = raw[3]
    for tag in raw[4]:
        s2 = ET.SubElement(r, 's', n=tag)
    a = ET.tostring(e).decode('utf-8').replace('!!!!!', '<b/>').replace('%%%%%', '<g>').replace('#####', '</g>')
    print(unescape(a))


def main():
    with open(sys.argv[1]) as f:  # fao-dan entries
        fd = f.readlines()

    with open(sys.argv[2]) as g:  # dan-nor bidix
        dn = g.read().replace('<b/>', '!!!!!').replace('<g>', '%%%%%').replace('</g>', '#####')

    with open(sys.argv[3]) as inter:  # intersection
        pairs = [line.strip().split(';') for line in inter.read().strip().split('\n')]

    for pair in pairs:
        t = make_entries(pair, fd, dn)
        make_xml(t)

main()
