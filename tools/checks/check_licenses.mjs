#!/usr/bin/env node
// Kiểm tra giấy phép và SDK của web/ (TC-CP-01, TC-CP-02).
// Dùng: node tools/checks/check_licenses.mjs [đường-dẫn-tới-web]
// Thoát 1 nếu có gói ngoài allowlist, gói UNKNOWN/UNLICENSED, hoặc dependency
// trực tiếp chưa có dòng trong sdk-allowlist.md.
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const WEB = resolve(process.argv[2] ?? join(HERE, '..', '..', 'web'))
const ALLOW = new Set(
  readFileSync(join(HERE, 'license-allowlist.txt'), 'utf8')
    .split('\n').map((l) => l.trim()).filter(Boolean),
)
const SDK_DOC = readFileSync(join(HERE, 'sdk-allowlist.md'), 'utf8')
const pkg = JSON.parse(readFileSync(join(WEB, 'package.json'), 'utf8'))
const SELF = `${pkg.name}@${pkg.version}`

// "(MIT OR Apache-2.0)" -> ["MIT", "Apache-2.0"]. Một gói đạt khi MỌI mảnh đều
// nằm trong allowlist: chấp nhận mảnh yếu nhất là cách duy nhất an toàn khi
// không biết người dùng lại sẽ chọn nhánh nào.
const parts = (s) => String(s).replace(/[()]/g, '').split(/\s+(?:OR|AND)\s+/i).map((x) => x.trim()).filter(Boolean)
const ok = (s) => {
  const p = parts(s)
  return p.length > 0 && p.every((x) => ALLOW.has(x) || ALLOW.has(x.replace(/-\d.*$/, '')))
}

const raw = execFileSync('npx', ['--yes', 'license-checker', '--json'], {
  cwd: WEB, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, shell: process.platform === 'win32',
})
const tree = JSON.parse(raw)

const errs = []
let checked = 0
for (const [name, info] of Object.entries(tree)) {
  if (name === SELF) continue // gói của chính mình, private, không phát hành
  checked += 1
  const lic = info.licenses ?? 'UNKNOWN'
  if (/UNKNOWN|UNLICENSED/i.test(String(lic))) errs.push(`${name}: giấy phép ${lic}`)
  else if (!ok(lic)) errs.push(`${name}: ${lic} ngoài allowlist`)
}

// TC-CP-02: mọi dependency trực tiếp phải có dòng trong sdk-allowlist.md
const direct = [...Object.keys(pkg.dependencies ?? {}), ...Object.keys(pkg.devDependencies ?? {})]
const missing = direct.filter((d) => !SDK_DOC.includes(d))

console.log(`${checked} gói · ${errs.length} lỗi giấy phép · ${missing.length} gói thiếu dòng SDK`)
for (const e of errs) console.log('LỖI', e)
for (const m of missing) console.log('LỖI', `${m}: chưa có dòng trong tools/checks/sdk-allowlist.md`)
process.exit(errs.length + missing.length ? 1 : 0)
