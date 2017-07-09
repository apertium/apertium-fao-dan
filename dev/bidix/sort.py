import re
import sys

#'fao-nor-entries'

with open (sys.argv[1]) as f:
    entries = f.readlines()

entries.sort(key=lambda x: (re.match('<e.*?><p><l>.*?<(.*?)>', x).group(1),
                                     re.match('<e.*?><p><l>(.*?)<', x).group(1)))
for e in entries:
    print(e, end='')
