# P.1 delivery - 2026-09-24

Task: `P.1` · Plan: https://hub.yawasa.com/app/p/moonegg-p1-plan
Result: https://hub.yawasa.com/app/p/moonegg-p1-result · Record: `records/P.1.md`
Merge commit: `3378960` · Branch `chore/p1-repo-ci`, merged and deleted

This is the QC package: the raw output of every check, exactly as it was printed on the machine on
2026-09-24. Nothing here is retyped. The Result drop explains what the task did; this one proves it.

**Evidence scan before handover:** 0 findings. Patterns searched: JWT strings, `gho_` and `ghp_`
tokens, `sk-` keys, private key blocks, personal identity numbers.

## Cổng đầy đủ chạy ở máy

`evidence/gate-full.txt`

```
pytest tools/checks               dat
  verify_pack tren du lieu mau      dat
    30 bản ghi · 0 lỗi · 2 cảnh báo
  vitest                            dat
  cong giay phep (TC-CP-01/02)      dat
    49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
gate exit=0
```

## Bộ test python

`evidence/pytest.txt`

```
.....                                                                    [100%]
5 passed in 1.50s
exit=0
```

## TC-CP-01 và TC-CP-02 trên web/

`evidence/licences.txt`

```
49 gói · 0 lỗi giấy phép · 0 gói thiếu dòng SDK
exit=0
```

## Cổng từ chối một gói GPL-3.0

`evidence/licence-gate-bites.txt`

```
1 gói · 1 lỗi giấy phép · 1 gói thiếu dòng SDK
LỖI fake-gpl-pkg@1.0.0: GPL-3.0 ngoài allowlist
LỖI fake-gpl-pkg: chưa có dòng trong tools/checks/sdk-allowlist.md
exit=1
```

## Cấu hình cổng chung của máy

`evidence/devgate-doctor.txt`

```
hooksPath : C:/Users/HughNguyen/.config/devgate/hooks
repo      : D:/Projects/MoonEgg
cong repo : tools/checks/gate.sh
```

## Nguyên văn GitHub từ chối chạy Actions

`evidence/github-actions-blocked.txt`

```
The job was not started because recent account payments have failed or your spending limit needs to be increased. Please check the 'Billing & plans' section in your settings
```

## Kết quả quét bằng chứng trước khi giao

`evidence/scan.txt`

```
Quet ngay 2026-09-24: 0
0 phat hien.
Mau tim: JWT, gho_/ghp_, sk-, private key, so dinh danh ca nhan.
```

## What a reader should take from this

- The gate runs in about five seconds and refuses a commit that breaks a test.
- The licence gate rejects a package the project may not ship, proven against a GPL fixture.
- The data checker reports the data, not the console encoding, which was a real bug before P.1.
- GitHub Actions never ran: the account is blocked on billing, which is why the gate moved here.
