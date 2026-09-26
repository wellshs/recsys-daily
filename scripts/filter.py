import json,re,csv,os,collections,shutil
p=json.load(open('papers_all.json')); aff=json.load(open('aff2021.json')); aff26=json.load(open('aff2026.json')); aw_old=json.load(open('awards_2016_2020.json'))
AW21={
 2021:[("Best Paper","An Audit of Misinformation Filter Bubbles on YouTube"),("Best Student Paper","Pessimistic Reward Models for Off-Policy Learning"),("Best Demo","Connecting Students with Research Advisors")],
 2022:[("Best Paper","Denoising Self-Attentive Sequential Recommendation"),("Best Paper Runner-up","RADio"),("Best Student Paper","Exploring the longitudinal effect of nudging"),("Best Student Paper Runner-up","Modeling Two-Way Selection"),("Best Demo","RecPack")],
 2023:[("Best Full Paper","gSASRec"),("Best Full Paper Runner-up","Going Beyond Local: Global Graph-Enhanced"),("Best Full Paper Runner-up","Pairwise Intent Graph Embedding"),("Best Short Paper","Interpretable User Retention Modeling"),("Best Short Paper Runner-up","Scalable Approximate NonSymmetric Autoencoder"),("Best Short Paper Runner-up","Of Spiky SVDs")],
 2024:[("Best Full Paper","Towards Empathetic Conversational Recommender"),("Best Short Paper","The MovieLens Beliefs Dataset"),("Best Student Paper","Unlocking the Hidden Treasures")],
 2025:[("Best Full Paper","You Don"),("Best Short Paper","Beyond Top-1")],
}
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
for x in p:
    x['award']=''
    for a,pref in AW21.get(x['year'],[]):
        if norm(x['title']).startswith(norm(pref)): x['award']=a
for y,lst in AW21.items():
    for a,pref in lst:
        if not any(x['award']==a and norm(x['title']).startswith(norm(pref)) for x in p): print('AWARD NOT MATCHED',y,a,pref)
BIG={
 'Google':r'google|deepmind|youtube|waymo',
 'Meta':r'\bmeta\b|facebook|instagram|whatsapp|\bfair\b',
 'Amazon':r'amazon|\baws\b|twitch|audible|zappos',
 'Microsoft':r'microsoft|\bmsr\b|linkedin|github',
 'Apple':r'\bapple\b',
 'Netflix':r'netflix',
 'Spotify':r'spotify',
 'NVIDIA':r'nvidia',
 'Pinterest':r'pinterest',
 'Uber':r'\buber\b',
 'Airbnb':r'airbnb',
 'Snap':r'\bsnap\b|snapchat',
 'X/Twitter':r'twitter|\bx corp',
 'eBay':r'\bebay\b',
 'Booking/Expedia':r'booking\.com|booking holdings|expedia',
 'Roblox':r'roblox',
 'Salesforce':r'salesforce',
 'Adobe':r'adobe',
 'IBM':r'\bibm\b',
 'Intel':r'\bintel\b',
 'Yahoo':r'yahoo',
 'Criteo':r'criteo',
 'ByteDance/TikTok':r'bytedance|tiktok|douyin',
 'Alibaba':r'alibaba|taobao|alipay|ant group|ant financial|lazada|damo|tmall|alimama|ele\.me',
 'Tencent':r'tencent|wechat',
 'Baidu':r'baidu',
 'Kuaishou':r'kuaishou|kwai',
 'Meituan':r'meituan',
 'JD':r'\bjd\.com|\bjd\b|jingdong',
 'Huawei':r'huawei|noah',
 'Xiaomi':r'xiaomi',
 'NetEase':r'netease',
 'Shopee/Sea':r'shopee|sea group|\bsea ltd',
 'Grab':r'\bgrab\b',
 'Naver':r'naver|\bline corp|line plus|\bline\b(?! [a-z]*graph)|clova',
 'Kakao':r'kakao',
 'Coupang':r'coupang',
 'Samsung':r'samsung',
 'Rakuten':r'rakuten',
 'Yandex':r'yandex',
 'Zalando':r'zalando',
 'SAP':r'\bsap\b',
 'Walmart':r'walmart|flipkart',
 'Disney/Hulu':r'disney|\bhulu\b',
 'Bloomberg':r'bloomberg',
 'Sony':r'\bsony\b',
 'Deezer':r'deezer',
 'Etsy':r'\betsy\b',
 'Instacart/DoorDash':r'instacart|doordash',
 'Mercado Libre':r'mercado ?libre|mercadolibre',
 'Wayfair':r'wayfair',
 'Roku':r'\broku\b',
 'Zillow':r'zillow',
 'ServiceNow':r'servicenow',
 'Oracle':r'\boracle\b',
 'Shopify':r'shopify',
 'Nike':r'\bnike\b',
 'Indeed/Glassdoor':r'\bindeed\b|glassdoor',
}
def companies(s):
    s=s.lower(); out=[]
    for k,rx in BIG.items():
        if re.search(rx,s): out.append(k)
    return out
rows=[]
for x in p:
    src=x['authors']
    if x['year']==2021:
        a=aff.get(x['doi'],{}); src=' ; '.join(a.get('inst',[])+a.get('raw',[]))
        src=x["authors"]+" ; "+src; x["affil_src"]=src
    if x['year']==2026:
        src=x['authors']+' ; '+' ; '.join(aff26.get(x['doi'],[])); x['affil_src']=src
    x['bigtech']=companies(src)
sel=[x for x in p if x['award'] or x['bigtech']]
print('selected',len(sel),'award',sum(1 for x in sel if x['award']),'bigtech',sum(1 for x in sel if x['bigtech']))
c=collections.Counter(k for x in sel for k in x['bigtech']); print(c.most_common())
# 2021 with affil but no bigtech? show some 2021 industry authors to sanity check
json.dump(p,open('papers_all_tagged.json','w'),ensure_ascii=False,indent=1)
