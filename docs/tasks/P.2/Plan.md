# Plan - P.2 Supabase, R2, Pages

Status: **not started**, stopped at Gate A, waiting for review.
Task: `P.2` · Prompt: `prompts/phase-P/P.2.md` · Record: `records/P.2.md`
Branch: `chore/p2-supabase-r2-pages`, cut from `main` at `789b9c4`.
Reviewer: `self`
Type: **INFRA** - servers, storage and a static site. No product behaviour yet.
Level: **L2** - see the note below on why this is not L3
Repro: not applicable, this is not an ISSUE
User-visible behaviour: no Flow.md. INFRA, nothing a learner sees changes.
Refs: `docs/09` section 3P.1 row P.2 · `docs/07` sections 2 and 7.2 · `docs/01` sections 11 and 14 ·
Test TC-AU-04 · FR-30, FR-44 to FR-47
Depends on: P.1, done on 2026-09-24.

**Level note.** This task creates the server tables that every later sync task reads and writes, so
it touches shared infrastructure, which normally forces L3 and a report instead of code. It stays
L2 because the schema is not being designed here: `docs/07` section 7.2 already fixed the tables,
the columns and the access rules, and this task only puts that decided design onto a server. If
anything in the schema turns out to need a change, that change is L3 and gets its own task.

**Decisions log (2026-09-24):**
1. 2026-09-24 - Reviewer confirmed they already hold Cloudflare and Supabase accounts, so this task
   configures existing accounts rather than creating them.

Out of scope: writing any sync code (task 2.9), the backup file format (2.10), image sync, the
analytics pipeline, buying an Apple Developer account.

> **Language rule (B1/B2):** short sentences, 20 words or fewer. Active voice. One idea per sentence.

---

## 0. Does this task need a Flow.md?

No. Type is INFRA and no screen exists yet. Any deliberate behaviour note goes in section 5.

## 1. Goal

After this task the project has three addresses that later tasks can point at: a database that
stores one user's events and refuses to show them to anyone else, a bucket that serves content
files for free, and a web address that serves the app. A learner sees none of it today, but tasks
1.11, 2.9 and 2.10 cannot start without it.

## 2. Starting point, checked today

Commands were run today on this machine; the output below is real, not remembered.

| Thing | State today | Evidence |
| --- | --- | --- |
| `supabase` CLI | not installed | `command -v supabase` finds nothing |
| `wrangler` CLI | not installed | `command -v wrangler` finds nothing |
| `psql` | not installed | `command -v psql` finds nothing |
| `npx` | 11.6.2 | `npx --version` |
| `supabase/` in repo | does not exist | `ls -A supabase` returns "No such file or directory" |
| `.env.example` | does not exist | same command |
| Schema design | already decided | `docs/07-kien-truc.md:491` onward: 7 tables, RLS rule, delete rule |
| Sync contract | already decided | `docs/07-kien-truc.md:255` event enum, `:293` sync section |
| P.1 gate | in place | `tools/checks/gate.sh`, runs on every commit |

No CLI tool is installed, and none is required: Supabase SQL runs in the dashboard's SQL editor,
and the R2 bucket plus the Pages project are made in the Cloudflare dashboard. The work is mostly
reading a written script and clicking, which is why section 4.5 decides who clicks.

## 3. Flow

```mermaid
graph TB
    A["supabase/schema.sql in the repo"]:::cyan --> B["Supabase SQL editor"]:::amber
    B --> C["7 tables, index, RLS"]:::purple
    C --> D["TC-AU-04: user A cannot read user B"]:::green
    E["R2 bucket vocab-content"]:::purple --> F["curl one public file"]:::green
    G["Pages site, empty page"]:::purple --> H["URL answers 200"]:::green
    I["ping action every 3 days"]:::amber --> C

    classDef amber fill:transparent,stroke:#f4b860,stroke-width:2px,color:#fff
    classDef cyan fill:transparent,stroke:#7cc4ff,stroke-width:2px,color:#fff
    classDef green fill:transparent,stroke:#c4f47c,stroke-width:2px,color:#fff
    classDef purple fill:transparent,stroke:#c8a4ff,stroke-width:2px,color:#fff
```

Three addresses, one proof each, plus a heartbeat that stops the free project pausing.

## 4. Plan of work

### 4.1 `supabase/schema.sql` - required, written before anything is clicked

The whole schema lives in one file in the repo, not in the dashboard's history. It is written to be
run twice with the same result: `create table if not exists`, `create index if not exists`, and
policies dropped before they are created. The reason is section 5 row 3: a schema that only exists
in a dashboard cannot be reviewed, and cannot be rebuilt if the project is lost.

Tables, exactly as `docs/07` section 7.2 fixes them: `profile`, `device`, `review_event`,
`user_content`, `settings`, `sync_cursor`, `analytics_daily`. On `review_event`: `event_id` text
primary key, `server_seq` as `bigserial`, an index on `(user_id, server_seq)`, and a unique
constraint on `event_id`. `item_state`, `session_state` and the counter tables are deliberately not
here: `docs/07` says the server never needs them.

### 4.2 Row level security - required, the part that carries the risk

Every user table gets RLS enabled and a policy `user_id = auth.uid()` for select and insert.
`analytics_daily` gets insert only and holds no raw `user_id`. Enabling RLS and then forgetting one
policy is the mistake that looks fine and leaks everything, so section 7 tests it with two real
users rather than by reading the SQL.

**One more hole, found while reading this plan back.** A select and insert policy of
`user_id = auth.uid()` lets a client insert any value it likes into `server_seq`. That column is
the sync cursor: every device asks for "events after sequence N". A client that writes its own
sequence number, by accident or on purpose, can hide its events from its own next pull, or push
another device into re-reading everything. The column must be server-assigned only. The fix is a
`bigserial` default plus a `before insert` trigger that overwrites whatever the client sent, and a
test that proves it. Test 9 in section 7.

### 4.3 Auth providers - required

Google and email magic link get switched on. Apple is left off with a written reason: it needs an
Apple Developer account at 99 USD a year, which `docs/02` section 4 records as not bought. The
prompt for this task already allows this. A one-line TODO goes in the record, not a silent gap.

### 4.4 Cloudflare R2 and Pages - required

Bucket `vocab-content`, public read, proven with one `curl` against a real uploaded file. Pages
project pointing at `web/dist`, deployed empty, proven by a URL that answers 200. Nothing else is
configured: caching, custom domains and cache headers belong to task 1.11 and 2.11.

### 4.5 Who clicks - proposal, needs the reviewer's answer

Two ways to do the dashboard work:

| Way | What it costs | What it risks |
| --- | --- | --- |
| The reviewer clicks, following a written script | a few minutes of their time | nothing; they see what is created under their name |
| I run it with a Supabase access token and a Cloudflare API token | faster | two long-lived credentials handed over for a one-time setup |

Proposal: the reviewer clicks. This task runs once, the steps are short, and the alternative means
sharing credentials that would outlive the task. `supabase/schema.sql` and a numbered click list go
in the repo so the steps are exact and repeatable.

### 4.6 `.env.example` and secret handling - required

`.env.example` holds variable names and empty values only: `VITE_SUPABASE_URL`,
`VITE_SUPABASE_ANON_KEY`, `R2_PUBLIC_BASE`. The real `.env` is already ignored by `.gitignore:10`.
No real key goes into the repo, into a task record, into a drop, or into this conversation.

### 4.7 Keep-alive - required

A GitHub Action every three days that reads one row through the REST API with the anon key. A free
Supabase project pauses after a week of no activity, which `docs/03` section 3 records as a known
risk. **This is the one piece that needs GitHub Actions**, and Actions is blocked on this account
(P.1 record, evidence). Section 5 row 6 handles it.

### Options considered, not chosen

- Run the schema through the `supabase` CLI. Rejected: it would mean installing a tool and holding
  an access token, for one SQL file that the dashboard editor runs just as well.
- Skip `schema.sql` and click the tables together. Rejected: the schema would then exist only
  inside a service, with no review and no way to rebuild it.
- Turn on Apple sign-in now. Rejected: 99 USD a year for a provider no one can test until there is
  an iOS build.

### Do not touch

- `docs/07` section 7.2. If the schema is wrong, that is an L3 task, not a quiet edit here.
- `web/`, `tools/`, `golden/`, `content/`.
- Anything to do with sync logic. This task creates the place, not the traffic.

## 5. Situations and edge cases

| # | Situation | Expected behaviour |
| --- | --- | --- |
| 1 | `schema.sql` run twice | second run changes nothing and raises no error |
| 2 | RLS on, one policy missing | test in section 7 must fail, not pass quietly |
| 3 | Supabase project lost or rebuilt | `schema.sql` from the repo rebuilds it without the dashboard |
| 4 | Free project pauses after a week idle | the ping brings it back; if the ping cannot run, the record says so |
| 5 | Anon key leaks | it is a public key by design; RLS is what protects the data, not the key |
| 6 | GitHub Actions still blocked | the ping is committed but cannot run. Fall back to a local scheduled task, or accept the pause and wake the project by hand. Written into the record either way, never left as a silent gap |
| 7 | Apple sign-in asked for later | one provider switched on, no schema change |
| 8 | Two test users are needed for test 1 | created by hand in the Supabase dashboard with email and password, not through magic link, so no real mailbox is involved |
| 9 | Test users left behind after testing | both deleted at the end of the task, and the record says so. A test account in a real project is a real account |
| 10 | A client sends its own `server_seq` | the trigger overwrites it; test 9 proves the stored value is the server's, not the client's |

## 6. Impact - who else touches this

| Thing created | Consumer | Effect |
| --- | --- | --- |
| `supabase/schema.sql` | tasks 2.9, 2.10, 4.3 | new; the server contract for all of them |
| Supabase project URL, anon key | `web/` from task 2.9 | new; read from `.env` |
| R2 bucket `vocab-content` | tasks P.10, 1.7, 1.11 | new; content packs are uploaded there |
| Pages project | task 2.11 | new; the PWA is deployed there |
| `.env.example` | every later web task | new |
| `.github/workflows/` | the ping action | second workflow next to the dormant `ci.yml` |

Found by reading `prompts/phase-P/P.2.md`, `docs/07` section 7.2, and the P.10, 1.11 and 2.9 rows
of `records/TRACKING.md`.

## 7. Tests and Definition of Done

| # | Test | How to run | Expected result |
| --- | --- | --- | --- |
| 1 | TC-AU-04 | create two test users, insert one event each, read with user A's token | 0 rows belonging to B, and no 500 error |
| 2 | RLS really on | query `pg_tables` and `pg_policies` for the 7 tables | every user table has RLS on and at least one policy |
| 3 | Schema is repeatable | run `schema.sql` twice on a clean project | no error, same tables |
| 4 | R2 is readable | `curl -I` a file uploaded to the bucket | HTTP 200 and the right content type |
| 5 | Pages answers | `curl -I` the Pages URL | HTTP 200 |
| 6 | Unique event id | insert the same `event_id` twice | second insert rejected |
| 7 | Ping works | run the ping request by hand with the anon key | one row returned, HTTP 200 |
| 8 | No secret in the repo | the gate, plus a grep for key patterns | 0 findings |
| 9 | `server_seq` cannot be set by a client | insert an event with `server_seq = 999999` using a user token | the stored row has the server's next sequence, not 999999 |
| 10 | Test users cleaned up | list auth users at the end | the two test accounts are gone |

**Definition of done:**

- [ ] `supabase/schema.sql` in the repo, run twice on the real project with no error
- [ ] 7 tables exist, with the index and the unique constraint on `review_event`
- [ ] RLS on for every user table, proven by test 1 with two real users, not by reading SQL
- [ ] `server_seq` is server-assigned: a client value is overwritten, proven by test 9
- [ ] The two test users are deleted before the task closes
- [ ] Google and magic link sign-in work; Apple is off with a written reason
- [ ] R2 bucket answers a public `curl`; Pages URL answers 200
- [ ] `.env.example` has names and no values; no real key anywhere in the repo
- [ ] The ping either runs, or the record says exactly why it cannot and what replaces it
- [ ] `records/P.2.md` has a result line per step and the test table with real output
- [ ] The branch is merged into `main` with `gate.sh merge`, and deleted

## 8. After Gate B

Planned commit messages:

```
feature(P.2): add supabase schema with row level security
docs(P.2): add env example and the dashboard click list
feature(P.2): add supabase keep-alive action
```

Then close on this machine with `bash ~/.config/devgate/gate.sh merge chore/p2-supabase-r2-pages`,
delete the branch on both sides, and update `records/TRACKING.md`.

## 9. Open questions for the reviewer

1. **Who clicks the dashboards?** Section 4.5 proposes that you do it, following a written list, so
   no long-lived credentials change hands. Say the word if you would rather hand over tokens.
2. **Supabase region.** Singapore, `ap-southeast-1`, is the closest to Vietnam. Confirm, or name
   another.
3. **Project and bucket names.** Proposal: Supabase project `moonegg`, R2 bucket `vocab-content`
   as the prompt says, Pages project `moonegg`. Confirm or rename now, because renaming later
   changes every URL.
4. **The keep-alive, given Actions is blocked.** Three ways: fix the GitHub billing; run the ping
   from a Windows scheduled task on this machine; or accept that the project pauses and wake it by
   hand while there are no real users. Proposal: the third, for now, with the action committed and
   ready. It costs nothing and there is no user to disturb yet.
