import json, urllib.request, urllib.parse, time, re, difflib
p=json.load(open('papers_all.json'))
for x in p: x['track']=x['track'].replace('&#038;','&')
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
def lookup(title):
    q=urllib.parse.quote(title)
    url=f'https://api.crossref.org/works?query.bibliographic={q}&rows=3&select=DOI,title&mailto=wellshs999@gmail.com'
    try:
        d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'recsys-list/1.0'}),timeout=30))
    except Exception as e:
        return ''
    for it in d['message']['items']:
        t=(it.get('title') or [''])[0]
        if difflib.SequenceMatcher(None,norm(t),norm(title)).ratio()>0.92 and it['DOI'].startswith('10.1145/'):
            return it['DOI']
    return ''
n=0
for x in p:
    if not x['doi'] and x['year']<=2025:
        x['doi']=lookup(x['title']); n+=1; time.sleep(0.6)
        if n%20==0: print(n, flush=True)
json.dump(p,open('papers_all.json','w'),ensure_ascii=False,indent=1)
print('missing', sum(1 for x in p if not x['doi'] and x['year']<=2025))
awards=[
 (2016,"Best Paper","Local Item-Item Models for Top-N Recommendation","Evangelia Christakopoulou, George Karypis"),
 (2016,"Best Short Paper","Adaptive, Personalized Diversity for Visual Discovery","Choon Hui Teo, Houssam Nassif, Daniel Hill, Sriram Srinivasan, Mitchell Goodman, Vijai Mohan, S. V. N. Vishwanathan"),
 (2017,"Best Paper","Modeling the Assimilation-Contrast Effects in Online Product Rating Systems: Debiasing and Recommendations","Xiaoying Zhang, Junzhou Zhao, John C.S. Lui"),
 (2017,"Best Paper Runner-up","Translation-based Recommendation","Ruining He, Wang-Cheng Kang, Julian McAuley"),
 (2018,"Best Long Paper","Causal Embeddings for Recommendation","Stephen Bonner, Flavian Vasile"),
 (2018,"Best Long Paper Runner-up","Generation Meets Recommendation: Proposing Novel Items for Groups of Users","Thanh Vinh Vo, Harold Soh"),
 (2018,"Best Short Paper","Impact of Item Consumption on Assessment of Recommendations in User Studies","Benedikt Loepp, Tim Donkers, Timm Kleemann, Jürgen Ziegler"),
 (2018,"Best Short Paper Runner-up","HOP-rec: High-order Proximity for Implicit Recommendation","Jheng-Hong Yang, Chih-Ming Chen, Chuan-Ju Wang, Ming-Feng Tsai"),
 (2019,"Best Long Paper","Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches","Maurizio Ferrari Dacrema, Paolo Cremonesi, Dietmar Jannach"),
 (2019,"Best Short Paper","Pace My Race: Recommendations for Marathon Running","Jakim Berndsen, Barry Smyth, Aonghus Lawlor"),
 (2019,"Honorable Mention Short Paper","Quick and Accurate Attack Detection in Recommender Systems through User Attributes","Mehmet Aktukmak, Yasin Yilmaz, Ismail Uysal"),
 (2020,"Best Long Paper","Progressive Layered Extraction (PLE): A Novel Multi-Task Learning (MTL) Model for Personalized Recommendations","Hongyan Tang, Junning Liu, Ming Zhao, Xudong Gong"),
 (2020,"Best Long Paper Runner-up","Exploiting Performance Estimates for Augmenting Recommendation Ensembles","Gustavo Penha, Rodrygo L. T. Santos"),
 (2020,"Best Short Paper","ADER: Adaptively Distilled Exemplar Replay Towards Continual Learning for Session-based Recommendation","Fei Mi, Xiaoyu Lin, Boi Faltings"),
]
out=[]
for y,a,t,au in awards:
    out.append(dict(year=y,award=a,title=t,authors=au,doi=lookup(t))); time.sleep(0.6)
json.dump(out,open('awards_2016_2020.json','w'),ensure_ascii=False,indent=1)
for o in out: print(o['year'],o['award'],o['doi'])
