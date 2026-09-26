import json, csv, os, collections
OUT=os.path.expanduser('~/recsys-reading-challenge'); os.makedirs(OUT,exist_ok=True)
p=json.load(open('papers_all.json')); aw=json.load(open('awards_2016_2020.json'))
MAIN={'Papers','Long Papers','Full Papers','Short Papers','Reproducibility','PPF Papers','Resource'}
def trackkey(t):
    order=['Papers','Long Papers','Full Papers','Short Papers','Reproducibility','PPF Papers','Resource','Industry','R&P Notes','LBR','Demos','Demo','Doctoral']
    return order.index(t) if t in order else 99
p.sort(key=lambda x:(x['year'],trackkey(x['track']),x['title'].lower()))
rows=[]; i=0
for a in aw:
    i+=1; rows.append(dict(no=i,year=a['year'],track='Award',award=a['award'],title=a['title'],authors=a['authors'],doi=a['doi'],url=f"https://doi.org/{a['doi']}" if a['doi'] else '',status='',read_date='',notes=''))
for x in p:
    i+=1; rows.append(dict(no=i,year=x['year'],track=x['track'],award='',title=x['title'],authors=x['authors'],doi=x['doi'],url=f"https://doi.org/{x['doi']}" if x['doi'] else '',status='',read_date='',notes=''))
with open(f'{OUT}/papers.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows,open(f'{OUT}/papers.json','w'),ensure_ascii=False,indent=1)
# README
L=[]
L.append('# RecSys 논문 1일 1편 챌린지 목록\n')
L.append('출처: recsys.acm.org 각 연도 Accepted Contributions 페이지, Best Paper Awards 페이지(https://recsys.acm.org/best-papers/). DOI는 페이지 링크 또는 Crossref 조회로 채움.\n')
L.append(f'- 총 {len(rows)}편 (수상작 2016–2020: {len(aw)}편, 2021–2026 전체: {len(p)}편)')
L.append('- 관리용 데이터: `papers.csv` (status / read_date / notes 열을 채우며 진행)\n')
cnt=collections.Counter((x['year'],x['track']) for x in p)
L.append('## 연도·트랙별 편수\n')
L.append('| 연도 | '+' | '.join(sorted({t for _,t in cnt},key=trackkey))+' | 합계 |')
tr=sorted({t for _,t in cnt},key=trackkey)
L.append('|'+'---|'*(len(tr)+2))
for y in range(2021,2027):
    L.append(f'| {y} | '+' | '.join(str(cnt.get((y,t),'')) for t in tr)+f' | {sum(v for (yy,_),v in cnt.items() if yy==y)} |')
L.append('')
L.append('## 2016–2020 수상 논문\n')
for r in rows:
    if r['track']!='Award': continue
    link=f"[{r['title']}]({r['url']})" if r['url'] else r['title']
    L.append(f"- [ ] #{r['no']} ({r['year']}, {r['award']}) {link} — {r['authors']}")
L.append('')
for y in range(2021,2027):
    L.append(f'## RecSys {y}'+(' (2026-09-28 ~ 10-02 개최, 미출간)' if y==2026 else '')+'\n')
    for t in tr:
        items=[r for r in rows if r['year']==y and r['track']==t]
        if not items: continue
        L.append(f'### {t} ({len(items)})\n')
        for r in items:
            link=f"[{r['title']}]({r['url']})" if r['url'] else r['title']
            L.append(f"- [ ] #{r['no']} {link} — {r['authors']}")
        L.append('')
open(f'{OUT}/README.md','w').write('\n'.join(L))
print(len(rows),'rows ->',OUT)
