import json,csv,os,collections,shutil
OUT=os.path.expanduser('~/recsys-reading-challenge')
# keep the full list under full/
os.makedirs(f'{OUT}/full',exist_ok=True)
for f in ['papers.csv','papers.json','README.md']:
    if os.path.exists(f'{OUT}/{f}') and not os.path.exists(f'{OUT}/full/{f}'): shutil.move(f'{OUT}/{f}',f'{OUT}/full/{f}')
p=json.load(open('papers_all_tagged.json')); aw=json.load(open('awards_2016_2020.json'))
order=['Papers','Long Papers','Full Papers','Short Papers','Reproducibility','PPF Papers','Resource','Industry','R&P Notes','LBR','Demos','Demo','Doctoral']
tk=lambda t: order.index(t) if t in order else 99
sel=[x for x in p if x['award'] or x['bigtech']]
sel.sort(key=lambda x:(x['year'],0 if x['award'] else 1,tk(x['track']),x['title'].lower()))
rows=[];i=0
def url(d): return f'https://doi.org/{d}' if d else ''
for a in aw:
    i+=1; rows.append(dict(no=i,year=a['year'],track='Award',award=a['award'],bigtech='',title=a['title'],authors=a['authors'],doi=a['doi'],url=url(a['doi']),status='',read_date='',notes=''))
for x in sel:
    i+=1; rows.append(dict(no=i,year=x['year'],track=x['track'],award=x['award'],bigtech='; '.join(x['bigtech']),title=x['title'],authors=x['authors'],doi=x['doi'],url=url(x['doi']),status='',read_date='',notes=''))
with open(f'{OUT}/papers.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows,open(f'{OUT}/papers.json','w'),ensure_ascii=False,indent=1)
L=['# RecSys 논문 1일 1편 챌린지 목록 (수상작 + 빅테크 필터)\n',
 '필터 기준: (1) 2016–2026 Best Paper 계열 수상작(Best/Runner-up/Honorable Mention/Student/Demo), (2) 2021–2026 논문 중 저자 소속에 빅테크·대형 IT 기업이 포함된 것. 소속은 accepted-contributions 페이지의 저자 괄호 표기(2022–2025), OpenAlex(2021), Crossref(2026)로 판별. 전체 목록은 `full/`에 있음.\n',
 f'- 총 {len(rows)}편 (2016–2020 수상작 {len(aw)}편, 2021–2026 필터 통과 {len(sel)}편: 수상작 {sum(1 for x in sel if x["award"])}편, 빅테크 {sum(1 for x in sel if x["bigtech"])}편)',
 '- 관리용 데이터: `papers.csv` (status / read_date / notes 열)\n']
cnt=collections.Counter(x['year'] for x in sel)
L.append('## 연도별 편수\n\n| 연도 | 편수 | 수상 | 빅테크 |\n|---|---|---|---|')
for y in range(2021,2027): L.append(f'| {y} | {cnt[y]} | {sum(1 for x in sel if x["year"]==y and x["award"])} | {sum(1 for x in sel if x["year"]==y and x["bigtech"])} |')
cc=collections.Counter(k for x in sel for k in x['bigtech'])
L.append('\n## 기업별 편수 (중복 포함)\n\n| 기업 | 편수 |\n|---|---|')
for k,v in cc.most_common(): L.append(f'| {k} | {v} |')
L.append('\n## 2016–2020 수상 논문\n')
for r in rows:
    if r['track']=='Award': L.append(f"- [ ] #{r['no']} ({r['year']}, {r['award']}) [{r['title']}]({r['url']}) — {r['authors']}")
for y in range(2021,2027):
    L.append(f'\n## RecSys {y}'+(' (2026-09-28~10-02 개최, 수상작 미발표)' if y==2026 else '')+'\n')
    for t in order:
        items=[r for r in rows if r['year']==y and r['track']==t]
        if not items: continue
        L.append(f'### {t} ({len(items)})\n')
        for r in items:
            tag=(f" **[{r['award']}]**" if r['award'] else '')+(f" `{r['bigtech']}`" if r['bigtech'] else '')
            link=f"[{r['title']}]({r['url']})" if r['url'] else r['title']
            L.append(f"- [ ] #{r['no']}{tag} {link} — {r['authors']}")
        L.append('')
open(f'{OUT}/README.md','w').write('\n'.join(L))
print(len(rows),'rows'); print('\n'.join(L[4:14]))
