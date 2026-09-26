import re, html, json, sys
out=[]
for y in ['21','22','23','24','25','26']:
    t=open(f'acc{y}.html').read()
    i=t.find('<h1>Accepted Contributions'); body=t[i:]
    tabs=re.findall(r'<a href="#(content-tab-1-\d+)">([^<]*)</a>', body)
    tabmap=dict(tabs)
    # split content sections
    parts=re.split(r'<div id="(content-tab-1-\d+)" class="tabs-content"', body)
    for k in range(1,len(parts),2):
        tid=parts[k]; sec=parts[k+1]
        # cut at next major div end? sections are sequential; parts split handles it
        track=tabmap.get(tid,tid).strip()
        items=re.findall(r'<li>(.*?)</li>', sec, re.S)
        for it in items:
            if '<em>' not in it: continue
            # abstract
            abst=''
            m=re.search(r'<div style="display: none;">\s*<p>(.*?)</p>', it, re.S)
            if m: abst=html.unescape(re.sub(r'<[^>]+>','',m.group(1))).strip()
            head=it.split('<em>')[0]
            ptype=''
            pm=re.search(r'<span class=paper-type title=\'?"?([^>\'"]*)\'?"?>([A-Z]+)</span>', head)
            if pm: ptype=pm.group(1)
            doi=''
            dm=re.search(r'https?://(?:dx\.)?doi\.org/(10\.\d+/[\w.]+)', it) or re.search(r'dl\.acm\.org/doi/(?:abs/|full/)?(10\.\d+/[\w.]+)', it)
            if dm: doi=dm.group(1)
            title=html.unescape(re.sub(r'<[^>]+>','',re.sub(r'<span class=paper-type.*?</span>','',head))).strip()
            title=re.sub(r'\s+',' ',title)
            am=re.search(r'<em>(.*?)</em>', it, re.S)
            authors=html.unescape(re.sub(r'<[^>]+>','',am.group(1))).strip()
            authors=re.sub(r'^by\s+','',authors).rstrip('.')
            authors=re.sub(r'\s+',' ',authors)
            if not title: continue
            out.append(dict(year=2000+int(y),track=track,ptype=ptype,title=title,authors=authors,doi=doi,abstract=abst))
json.dump(out,open('papers_all.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
c=Counter((p['year'],p['track']) for p in out)
for k in sorted(c): print(k,c[k])
print('total',len(out))
