import cmudict, json, csv, sqlite3
from nltk.corpus import wordnet as wn

CMU = cmudict.dict()
# ARPAbet -> IPA (US)
A2I = {'AA':'ɑ','AE':'æ','AH':'ʌ','AO':'ɔ','AW':'aʊ','AY':'aɪ','B':'b','CH':'tʃ','D':'d','DH':'ð','EH':'ɛ','ER':'ɝ','EY':'eɪ','F':'f','G':'ɡ','HH':'h','IH':'ɪ','IY':'i','JH':'dʒ','K':'k','L':'l','M':'m','N':'n','NG':'ŋ','OW':'oʊ','OY':'ɔɪ','P':'p','R':'r','S':'s','SH':'ʃ','T':'t','TH':'θ','UH':'ʊ','UW':'u','V':'v','W':'w','Y':'j','Z':'z','ZH':'ʒ'}
# ARPAbet -> 12 viseme (sil PP FF TH DD SS CH aa E I O U)
A2V = {'P':'PP','B':'PP','M':'PP','F':'FF','V':'FF','TH':'TH','DH':'TH','T':'DD','D':'DD','N':'DD','L':'DD','K':'DD','G':'DD','NG':'DD','HH':'DD','Y':'I','S':'SS','Z':'SS','SH':'CH','ZH':'CH','CH':'CH','JH':'CH','R':'O','W':'U','AA':'aa','AE':'aa','AH':'aa','AY':'aa','AW':'aa','AO':'O','OW':'O','OY':'O','EH':'E','EY':'E','ER':'E','IH':'I','IY':'I','UH':'U','UW':'U'}
# âm khó với người Việt
HARD = {'TH':'θ','DH':'ð','SH':'ʃ','ZH':'ʒ','R':'r','CH':'tʃ','JH':'dʒ'}
FINAL_HARD = {'S','Z','T','D','K','P','B','V','F','L','NT','ST','ND'}

def strip(p): return ''.join(c for c in p if not c.isdigit())
def stress_idx(ph):
    vowels=[i for i,p in enumerate(ph) if p[-1].isdigit()]
    for n,i in enumerate(vowels):
        if ph[i].endswith('1'): return n  # 0-based syllable index
    return 0
def ipa(ph):
    out=[]; vow=[i for i,p in enumerate(ph) if p[-1].isdigit()]
    for i,p in enumerate(ph):
        if p.endswith('1'): out.append('ˈ')
        out.append('ə' if p=='AH0' else A2I[strip(p)])
    return '/'+''.join(out)+'/'
def hard_flags(ph):
    flags=set()
    for p in ph:
        s=strip(p)
        if s in HARD: flags.add(HARD[s])
    last=strip(ph[-1]); last2=''.join(strip(x) for x in ph[-2:])
    if last2 in FINAL_HARD: flags.add('cuối '+last2.lower())
    elif last in FINAL_HARD: flags.add('cuối /'+A2I[last]+'/')
    return sorted(flags)
def visemes(ph):  # thứ tự viseme, timing lấy từ MFA sau
    return [A2V[strip(p)] for p in ph]

# 30 từ test; (headword, pos, freq_rank, variant index in CMUdict, nghĩa Việt tạm)
WORDS = [("hello","interj",12,0),("market","n",480,0),("umbrella","n",1910,0),("bargain","n",2340,0),
 ("reluctant","adj",1240,0),("think","v",95,0),("sink","v",3100,0),("wind","n",610,1),("wind","v",4200,0),
 ("receipt","n",2700,0),("go","v",30,0),("buy","v",210,0),("yesterday","adv",640,0),("cold","adj",300,0),
 ("egg","n",1200,0),("leave","v",150,0),("budget","n",1500,0),("approve","v",1900,0),("boss","n",1100,0),
 ("thorough","adj",2900,0),("through","prep",60,0),("climb","v",1800,0),("kitchen","n",900,0),("kettle","n",4300,0),
 ("stove","n",4100,0),("exhausted","adj",2600,0),("energetic","adj",3900,0),("decision","n",400,0),("rain","n",700,0),("mother","n",180,0)]

rows=[]; seen={}
for hw,pos,rank,vi in WORDS:
    prons=CMU.get(hw)
    if not prons: print("MISSING",hw); continue
    ph=prons[min(vi,len(prons)-1)]
    seen[hw]=seen.get(hw,0)+1
    item_id=f"w:{hw}#{seen[hw]}"
    wnpos={'n':'n','v':'v','adj':'a','adv':'r'}.get(pos)
    syn=wn.synsets(hw,pos=wnpos) if wnpos else []
    defs=[s.definition() for s in syn[:3]]
    synonyms=sorted({l.name().replace('_',' ') for s in syn[:3] for l in s.lemmas() if l.name().lower()!=hw})[:8]
    rows.append(dict(item_id=item_id,headword=hw,pos=pos,freq_rank=rank,arpabet=' '.join(ph),ipa_us=ipa(ph),
        stress_index=stress_idx(ph),hard_sound_flags=';'.join(hard_flags(ph)),viseme_seq=' '.join(visemes(ph)),
        wn_defs=' | '.join(defs),wn_synonyms=';'.join(synonyms),n_variants=len(prons),
        source='cmudict(BSD);wordnet(Princeton)',license='BSD;WordNet'))

with open('lexicon_raw_test.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
con=sqlite3.connect('lexicon_raw_test.sqlite'); con.execute('drop table if exists word')
con.execute('create table word(item_id text primary key, headword, pos, freq_rank int, arpabet, ipa_us, stress_index int, hard_sound_flags, viseme_seq, wn_defs, wn_synonyms, n_variants int, source, license)')
con.executemany('insert into word values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[tuple(r.values()) for r in rows]); con.commit()
print(f"{len(rows)} từ")
for r in rows[:9]+[rows[19],rows[20]]:
    print(f"{r['item_id']:16} {r['ipa_us']:16} nhấn={r['stress_index']} khó=[{r['hard_sound_flags']}] viseme={r['viseme_seq']}")
print("\nví dụ WordNet:", rows[4]['wn_defs'][:120]); print("đồng nghĩa (loại khỏi nhiễu):", rows[4]['wn_synonyms'])
# báo cáo phủ
print("\nPhủ: có IPA", sum(1 for r in rows), "/", len(rows), "; có nghĩa WordNet", sum(1 for r in rows if r['wn_defs']), "; đa cách đọc", sum(1 for r in rows if r['n_variants']>1))
