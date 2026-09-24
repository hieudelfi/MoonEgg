#!/usr/bin/env python3
"""Xác minh dữ liệu từ vựng trước khi đóng gói (TC-CT-01, 03, 05, 07 mức tối thiểu).
Dùng: python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv [--strict]
Thoát mã 1 nếu có lỗi. Mở rộng dần theo docs/08-kiem-thu.md §6.1."""
import csv, sys, sqlite3, os, collections

# Console Windows mặc định cp1252 không mã hoá được tiếng Việt: print sẽ ném
# UnicodeEncodeError và script thoát 1 dù dữ liệu không lỗi. Ép UTF-8 cho đầu ra
# của chính script để mã thoát nói về dữ liệu, không nói về code page.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ALLOW = {l.strip() for l in open(os.path.join(os.path.dirname(__file__),'license-allowlist.txt')) if l.strip()}
VISEMES = {'sil','PP','FF','TH','DD','SS','CH','aa','E','I','O','U'}

def load(path):
    if path.endswith('.csv'):
        return list(csv.DictReader(open(path, newline='', encoding='utf-8')))
    con = sqlite3.connect(path); con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute('select * from word')]

def main(path, strict=False):
    rows = load(path); errs = []; warns = []
    ids = collections.Counter(r['item_id'] for r in rows)
    for k, n in ids.items():
        if n > 1: errs.append(f"item_id trùng: {k} ({n})")
    for r in rows:
        i = r['item_id']
        if not r.get('ipa_us'): errs.append(f"{i}: thiếu IPA")
        if not r.get('arpabet'): errs.append(f"{i}: thiếu ARPAbet")
        lic = {x.strip() for x in (r.get('license') or '').replace(';', ',').split(',') if x.strip()}
        if not lic: errs.append(f"{i}: thiếu license")
        elif not lic <= ALLOW: errs.append(f"{i}: license ngoài allowlist {lic - ALLOW}")
        if not r.get('source'): errs.append(f"{i}: thiếu source")
        vs = (r.get('viseme_seq') or '').split()
        bad = [v for v in vs if v not in VISEMES]
        if bad: errs.append(f"{i}: viseme lạ {bad}")
        if strict:
            if not r.get('gloss_vi'): errs.append(f"{i}: thiếu nghĩa Việt")
            if int(r.get('n_examples', 0) or 0) < 2: errs.append(f"{i}: < 2 câu ví dụ")
            if r.get('review_status') != 'approved': errs.append(f"{i}: chưa approved")
        elif not r.get('wn_defs'): warns.append(f"{i}: WordNet không có nghĩa (cần kaikki)")
    # đồng tự khác âm: cùng headword phải khác arpabet
    by_hw = collections.defaultdict(list)
    for r in rows: by_hw[r['headword']].append(r['arpabet'])
    for hw, ps in by_hw.items():
        if len(ps) > 1 and len(set(ps)) < len(ps): errs.append(f"{hw}: các biến thể có cùng ARPAbet")
    print(f"{len(rows)} bản ghi · {len(errs)} lỗi · {len(warns)} cảnh báo")
    for e in errs: print("LỖI", e)
    for w in warns: print("CẢNH BÁO", w)
    return 1 if errs else 0

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sys.exit(main(args[0], strict='--strict' in sys.argv))
