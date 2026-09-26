#!/usr/bin/env python3
"""papers.csv 각 행에 arxiv_id / pdf_url 열을 채운다 (arXiv 제목 검색 → Semantic Scholar openAccessPdf)."""
import csv, re, json, time, urllib.request, urllib.parse, difflib, sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=list(csv.DictReader(open(f'{ROOT}/papers.csv',encoding='utf-8')))
for r in rows:
    r.setdefault('arxiv_id',''); r.setdefault('pdf_url','')
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
def get(url,timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'recsys-daily/1.0 (mailto:wellshs999@gmail.com)'}),timeout=timeout).read().decode('utf-8','ignore')
def arxiv(title):
    q=urllib.parse.quote(f'ti:"{re.sub(r"[^A-Za-z0-9 ]"," ",title)}"')
    try: x=get(f'http://export.arxiv.org/api/query?search_query={q}&max_results=5')
    except Exception: return ''
    for m in re.finditer(r'<entry>(.*?)</entry>',x,re.S):
        e=m.group(1); t=re.sub(r'\s+',' ',re.search(r'<title>(.*?)</title>',e,re.S).group(1)).strip()
        if difflib.SequenceMatcher(None,norm(t),norm(title)).ratio()>0.9:
            return re.search(r'<id>http://arxiv.org/abs/(.*?)</id>',e).group(1)
    return ''
def s2(doi):
    try: d=json.loads(get(f'https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf'))
    except Exception: return ''
    return (d.get('openAccessPdf') or {}).get('url','') or ''
n=0
for r in rows:
    if r['arxiv_id'] or r['pdf_url']: continue
    a=arxiv(r['title']); time.sleep(3.1)
    if a: r['arxiv_id']=a; r['pdf_url']=f'https://arxiv.org/pdf/{a}'
    elif r['doi']:
        u=s2(r['doi']); time.sleep(1.2)
        if u: r['pdf_url']=u
    n+=1
    if n%25==0:
        print(n,'done;',sum(1 for x in rows if x['pdf_url']),'with pdf',flush=True)
        with open(f'{ROOT}/papers.csv','w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),lineterminator='\n'); w.writeheader(); w.writerows(rows)
with open(f'{ROOT}/papers.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()),lineterminator='\n'); w.writeheader(); w.writerows(rows)
print('final:',sum(1 for x in rows if x['arxiv_id']),'arxiv;',sum(1 for x in rows if x['pdf_url']),'pdf_url total')
