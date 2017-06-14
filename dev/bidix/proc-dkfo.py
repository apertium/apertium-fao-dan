import sys;
import xml.etree.ElementTree as ET;
import re;

#	  <GR GRID="4231" ID="{6F0FE82D-01C2-4E97-A3BB-BCF424093DEE}">
#	    <STIG>0</STIG>
#	    <VERSIONS>
#	      <VS>
#	        <VS_NO>0</VS_NO>
#	        <VS_USER/>
#	        <VS_DATE/>
#	      </VS>
#	      <VS>
#	        <VS_NO>1</VS_NO>
#	        <VS_USER>hp</VS_USER>
#	        <VS_DATE>1995-09-21</VS_DATE>
#	      </VS>
#	    </VERSIONS>
#	    <L>
#	      <LEI>belysning</LEI>
#	      <HNR/>
#	    </L>
#	    <B>-en, -er</B>
#	    <M>ljós; lampa, ljósføri, ljósgøgn, ljósbúnaður;</M>
#	    <D>elektrisk ~</D>
#	    <M>elektriskt ljós;</M>
#	    <D>skiftende ~</D>
#	    <M>(um)skiftandi ljós;</M>
#	    <D>~er og skærme til salg</D>
#	    <M>lampur og skermar til sølu;</M>
#	    <N2>(flutt m.)</N2>
#	    <D>til ~ af sagen</D>
#	    <M>til (tess) at greiða málið</M>
#	  </GR>
#	

def parse_entry(line): #{
	entries = [];
	big = line.split(';');
	id = 0;
	for b in big: #{
		small = b.split(',');
		for s in small: #{
			entries.append((id, s.strip()));	
		#}
		id += 1;
	#}
	return entries;
#}

### Usage:
## python3 proc-dkfo.py dkfo_010.xml  ~/source/apertium/languages/apertium-dan/apertium-dan.dan.dix ~/source/giellatekno/langs/fao/src/morphology/lexicon.tmp.lexc 

doc = ET.parse(sys.argv[1]);
dix = ET.parse(sys.argv[2]);
#langs/fao/src/morphology/lexicon.tmp.lexc
lex = open(sys.argv[3]).readlines();

danord = {};
faoord = {};

for e in dix.findall('.//e'): #{
	if 'lm' in e.attrib: #{
		lm = e.attrib['lm'];
		if lm not in danord: #{
			danord[lm] = [];
		#}
		for par in e.findall('.//par'): #{
			danord[lm].append(par.attrib['n'])
		#}
	#}
#}

for line in lex: #{
	if line.strip() == '': continue;
	if line.count('+') > 0: continue;
	if line.strip()[-1] != ';': continue;
	if line.strip()[0] == '!': continue;
	if line.count('% ') > 0: continue;

	row = line.split(' ');
	if len(row) < 2: #{
		continue;
	#}

	lm = '';
	if row[0].count(':') > 0: #{
		lm = row[0].split(':')[0];	
	else: #{
		lm = row[0];
	#}
	if lm not in faoord: #{
		faoord[lm] = [];
	#}
	faoord[lm].append(row[1]);
#}

for p in doc.findall('.//GR'): #{
	dan = p.findall('.//LEI')[0].text
	found = '-';
	pardef = '_';
	tag = 'x.';
	tags = p.findall('.//K');
	if tags: #{
		tag = p.findall('.//K')[0].text
	#}

	if dan in danord: #{
		found = '+';
		if len(danord[dan]) == 1: #{
			pardef = danord[dan][0];
		#}
	#}

	entries = p.findall('.//M');
	if entries: #{
		if not entries[0].text: #{
			continue;
		#}
		for e in parse_entry(entries[0].text): #{
			flm = e[1].strip();
			if flm == '': continue;
			fpar = '_';
			if flm in faoord: #{
				if len(faoord[flm]) == 1: #{
					fpar = faoord[flm][0];
					if found == '+': found = '#';
				#}
			#}
			print('%s\t%s\t%s\t%s\t%d\t%s\t%s' % (found, dan, pardef, tag, e[0], e[1], fpar));
		#}
	#}
#}
