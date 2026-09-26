#!/usr/bin/env python3
"""papers.csv를 읽어 docs/index.html(진행 현황 + 오늘의 논문)을 생성한다."""
import csv, os, html, datetime, collections
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=list(csv.DictReader(open(f'{ROOT}/papers.csv',encoding='utf-8')))
done=[r for r in rows if r['status']]
todo=[r for r in rows if not r['status']]
done.sort(key=lambda r:(r['read_date'],int(r['order'])),reverse=True)
esc=html.escape
def item(r,link=True):
    tags=''.join(f'<span>{esc(t)}</span>' for t in filter(None,[r['award'],*(r['bigtech'].split('; ') if r['bigtech'] else []),str(r['year'])]))
    title=esc(r['title'])
    if link and r['notes']: title=f'<a href="{esc(r["notes"].replace("docs/",""))}">{title}</a>'
    date=f'<span class="meta">{esc(r["read_date"])}</span> ' if r['read_date'] else ''
    return f'<li>{date}<b>#{r["order"]}</b> {title}<div class="chips">{tags}</div></li>'
phase_names={'1-award-2016-2020':'1단계 · 2016–2020 수상작','2-award-2021-2026':'2단계 · 2021–2026 수상작','3-bigtech':'3단계 · 빅테크 논문 (주제별)'}
prog=collections.Counter(r['phase'] for r in done); tot=collections.Counter(r['phase'] for r in rows)
today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d')
latest=done[0] if done else None
H=['<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>RecSys Daily</title>',
   open(f'{ROOT}/docs/template.html').read().split('<style>')[1].split('</style>')[0].join(['<style>','</style>']),
   '</head><body><main>',
   f'<h1>RecSys 논문 1일 1편</h1><p class="meta">갱신 {today} · 진행 {len(done)}/{len(rows)}편</p>']
if latest:
    H.append(f'<div class="callout"><b>최신</b> {latest["read_date"]}<br><a href="{esc(latest["notes"].replace("docs/",""))}">#{latest["order"]} {esc(latest["title"])}</a></div>')
if todo:
    H.append(f'<p class="meta">다음 예정: #{todo[0]["order"]} {esc(todo[0]["title"])}</p>')
H.append('<h2>단계별 진행</h2><ul>'+''.join(f'<li>{esc(v)}: {prog[k]}/{tot[k]}</li>' for k,v in phase_names.items())+'</ul>')
H.append('<h2>읽은 논문</h2><ul>'+''.join(item(r) for r in done)+'</ul>')
H.append('<h2>남은 논문</h2><details><summary>목록 펼치기 ('+str(len(todo))+'편)</summary><ul>'+''.join(item(r,link=False) for r in todo)+'</ul></details>')
H.append('</main></body></html>')
open(f'{ROOT}/docs/index.html','w',encoding='utf-8').write('\n'.join(H))
print('index:',len(done),'done /',len(rows))
