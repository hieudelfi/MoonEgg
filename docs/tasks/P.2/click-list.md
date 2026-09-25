# Click list - P.2 Supabase, R2, Pages

Task `P.2`. Plan: https://hub.yawasa.com/app/p/moonegg-p2-plan

This is the part of P.2 that happens in a browser. You run it, not me: Gate A decision 2 says
no access token and no API token changes hands.

Each step says what to click and what should be on screen afterwards. If a screen does not match,
stop at that step and say which one. Do not guess your way past it.

**What is safe to send back to me:** the project URL, the anon key, the R2 public base URL, the
Pages URL. All four are public by design.
**What must never be sent:** the database password, the `service_role` key, any Google OAuth client
secret. If one of those ends up in the chat by accident, rotate it in the dashboard.

Total: about 30 minutes, most of it in part A3 (Google sign-in).

---

## Part A - Supabase

### A1. Create the project

1. Open https://supabase.com/dashboard and sign in.
2. **New project**. Organisation: your own.
3. Name: `moonegg`
4. Database password: press **Generate a password**, then save it in your password manager.
   You will not need it again in this task.
5. Region: **Southeast Asia (Singapore)** - `ap-southeast-1`. Gate A decision 3.
6. Plan: **Free**.
7. **Create new project**, then wait about two minutes.

**On screen after:** the project home page, with a green dot next to the project name.

### A2. Copy the two public values

1. Left sidebar, bottom: **Project Settings** -> **API Keys** (older layouts: **API**).
2. Copy **Project URL**. It looks like `https://abcdefghijklm.supabase.co`.
3. Copy the **anon** / **public** key. It is a long string starting `eyJ`.
4. Do **not** copy the `service_role` key. It bypasses row level security and belongs nowhere
   outside that page.

**On screen after:** you hold two values. Paste them into a scratch note for now.

### A3. Turn on sign-in methods

**Email magic link** - two clicks:

1. **Authentication** -> **Sign In / Providers** -> **Email**.
2. Make sure **Enable email provider** is on. Leave **Confirm email** on.
3. **Save**.

**Google** - this is the long one, because Google needs its own project:

4. Open https://console.cloud.google.com in a second tab. Create a project named `moonegg`
   if you have none.
5. **APIs & Services** -> **OAuth consent screen**. User type **External**. App name `MoonEgg`,
   your email as support and developer contact. Save through to the end. Leave it in **Testing**.
6. **APIs & Services** -> **Credentials** -> **Create credentials** -> **OAuth client ID**.
   Application type: **Web application**. Name: `MoonEgg web`.
7. Back in Supabase, **Authentication** -> **Sign In / Providers** -> **Google**. Copy the
   **Callback URL** shown there. It ends in `/auth/v1/callback`.
8. Paste that URL into Google's **Authorised redirect URIs**, then **Create**.
9. Google shows a client ID and a client secret. Paste both into the Supabase Google provider,
   turn the provider **on**, and **Save**. The secret stays in that form; it does not come to me.

**Apple** - leave it off. Gate A: it needs an Apple Developer account at 99 USD a year, and
nothing can test it until there is an iOS build. This is a written decision, not an oversight.

**On screen after:** the provider list shows Email **Enabled** and Google **Enabled**, Apple off.

### A4. Run the schema

1. **SQL Editor** -> **New query**.
2. Open `supabase/schema.sql` from the repo. Copy all of it. Paste it in.
3. **Run**.

**On screen after:** `Success. No rows returned`.

4. **Run it a second time without changing anything.** This is test 3: the file has to be
   repeatable, so that a lost project can be rebuilt from the repo.

**On screen after:** `Success. No rows returned` again. Any red error here is a real failure -
stop and tell me the message.

### A5. Check the tables arrived

1. **Table Editor**. The schema picker should show `public`.

**On screen after:** seven tables - `analytics_daily`, `device`, `profile`, `review_event`,
`settings`, `sync_cursor`, `user_content`. Each row in the list shows an **RLS enabled** badge.

### A6. Create the two test users

These exist only to prove that user A cannot read user B. Part E deletes them. A test account in
a real project is a real account, so it does not get to stay.

1. **Authentication** -> **Users** -> **Add user** -> **Create new user**.
2. Email `p2-test-a@moonegg.invalid`, password `MoonEggP2-TestA`, tick **Auto Confirm User**.
3. Repeat for `p2-test-b@moonegg.invalid`, password `MoonEggP2-TestB`.

The `.invalid` domain cannot receive mail, which is the point: no real mailbox is touched, and
auto-confirm means none is needed.

**On screen after:** two users in the list, both with a confirmation date.

---

## Part B - Cloudflare R2

### B1. Create the bucket

1. Open https://dash.cloudflare.com -> **R2 Object Storage**.
2. If R2 has never been used on this account, it asks you to add a payment card. The free tier
   still costs nothing, but the card is required to open R2 at all. If you would rather not,
   stop here and tell me - P.10 and 1.7 need the bucket, so we would have to pick another host.
3. **Create bucket**. Name: `vocab-content`. Location: **Asia-Pacific (APAC)**.
4. **Create bucket**.

**On screen after:** the bucket page, empty, zero objects.

### B2. Make it public

1. In the bucket: **Settings** -> **Public Development URL** -> **Enable**.
2. Confirm. Cloudflare warns that anyone with the link can read the files. That is intended:
   this bucket holds content packs, not user data.
3. Copy the URL. It looks like `https://pub-<hex>.r2.dev`.

**On screen after:** Public Development URL shows **Enabled** plus that address.

### B3. Upload one file to prove it reads

1. Back on the bucket **Objects** tab: **Upload** -> pick any small text file. Name it
   `ping.txt` if you can choose.

**On screen after:** one object in the list. Send me the public base URL and the object name;
test 4 is a `curl` I run from here.

---

## Part C - Cloudflare Pages

### C1. Create the Pages project

1. Cloudflare dashboard -> **Workers & Pages** -> **Create** -> **Pages** ->
   **Connect to Git**.
2. Authorise the Cloudflare GitHub app for `hieudelfi/MoonEgg` if it asks. The repo is private;
   the app needs to be granted that one repo, not all of them.
3. Project name: `moonegg`. Production branch: `main`.
4. Build settings:
   - Framework preset: **None**
   - Root directory: `web`
   - Build command: `npm run build`
   - Build output directory: `dist`
5. **Save and Deploy**.

**On screen after:** a build log. The first deploy builds the empty Vite starter from P.1, which
takes a minute or two and should end green.

6. Copy the URL. It looks like `https://moonegg.pages.dev`.

**On screen after:** you hold the Pages URL. Test 5 is a `curl` I run from here.

---

## Part D - Send these back to me

Paste this filled in:

```
SUPABASE_URL      = https://____.supabase.co
SUPABASE_ANON_KEY = eyJ____
R2_PUBLIC_BASE    = https://pub-____.r2.dev
R2_TEST_OBJECT    = ping.txt
PAGES_URL         = https://____.pages.dev
```

Then I run tests 1, 2, 4, 5, 6, 7 and 9 and write the real numbers into `records/P.2.md`.

I do **not** want, and will not store: the database password, the `service_role` key, the Google
client secret.

---

## Part E - After the tests, delete the test users

Do this only when I say the tests are done.

1. **Authentication** -> **Users**.
2. For `p2-test-a@moonegg.invalid` and `p2-test-b@moonegg.invalid`: three-dot menu ->
   **Delete user** -> confirm.

**On screen after:** neither address is in the list. That is test 10.
