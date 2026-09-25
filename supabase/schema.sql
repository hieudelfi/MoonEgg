-- MoonEgg server schema (Supabase / Postgres)
-- Task P.2. Design comes from docs/07-kien-truc.md section 7.2; this file only applies it.
-- Changing the shape of a table here is an L3 change: open a separate task, do not edit in place.
--
-- This file is idempotent. Running it twice on the same project changes nothing and raises
-- no error. Policies are dropped before they are created, because Postgres has no
-- "create policy if not exists".
--
-- Run it in the Supabase dashboard: SQL Editor -> New query -> paste -> Run.

-- ---------------------------------------------------------------------------
-- 1. Tables
-- ---------------------------------------------------------------------------

-- One row per account. deleted_at is set by account deletion (task 2.10) and kept
-- for 30 days to block abusive re-creation. It never holds learning data.
create table if not exists public.profile (
  user_id       uuid primary key references auth.users (id) on delete cascade,
  auth_provider text,
  created_at    timestamptz not null default now(),
  deleted_at    timestamptz
);

create table if not exists public.device (
  device_id uuid primary key,
  user_id   uuid not null references auth.users (id) on delete cascade,
  platform  text,
  last_seen timestamptz
);

-- The only table that grows with time. Append-only: RLS below grants select and
-- insert and nothing else, so update and delete are refused by default.
-- server_seq is the sync cursor every device reads. The server assigns it,
-- see section 3 below.
create table if not exists public.review_event (
  event_id   text primary key,
  user_id    uuid   not null references auth.users (id) on delete cascade,
  device_id  uuid,
  ts         bigint not null,
  type       text   not null,
  item_type  text,
  item_id    text,
  payload    jsonb,
  server_seq bigserial not null
);

create table if not exists public.user_content (
  content_id       text primary key,
  user_id          uuid not null references auth.users (id) on delete cascade,
  item_id          text,
  kind             text,
  text             text,
  local_image_path text,
  created_ts       bigint
);

-- A projection of the setting_changed events, kept so a new device can read
-- settings without replaying the whole log.
create table if not exists public.settings (
  user_id            uuid primary key references auth.users (id) on delete cascade,
  voice              text,
  daily_new          int,
  remind_times_json  text,
  topics_json        text,
  fsrs_params        jsonb,
  analytics_opt_out  boolean not null default false
);

-- Per-device sync position. docs/07 section 7.2 gives this table no user_id, so
-- its RLS rule reaches the owner through device instead. See section 2.
create table if not exists public.sync_cursor (
  device_id  uuid primary key references public.device (device_id) on delete cascade,
  pulled_seq bigint not null default 0,
  pushed_seq bigint not null default 0
);

-- Anonymous daily counters. user_hash is a one-way hash, never a raw user_id,
-- so nothing here can be traced back to an account.
create table if not exists public.analytics_daily (
  user_hash        text not null,
  day              date not null,
  sessions         int not null default 0,
  cards_seen       int not null default 0,
  reviews          int not null default 0,
  new_words        int not null default 0,
  seconds_studied  int not null default 0,
  streak_days      int not null default 0,
  primary key (user_hash, day)
);

-- Indexes. event_id is already unique: it is the primary key.
create index if not exists review_event_user_seq_idx
  on public.review_event (user_id, server_seq);

create index if not exists device_user_idx
  on public.device (user_id);

create index if not exists user_content_user_idx
  on public.user_content (user_id);

-- ---------------------------------------------------------------------------
-- 2. Row level security
-- ---------------------------------------------------------------------------
-- Every user table is closed by default and opened by one policy per action.
-- No update policy and no delete policy is deliberate: the event log is
-- append-only, and settings change by writing a new event.

alter table public.profile         enable row level security;
alter table public.device          enable row level security;
alter table public.review_event    enable row level security;
alter table public.user_content    enable row level security;
alter table public.settings        enable row level security;
alter table public.sync_cursor     enable row level security;
alter table public.analytics_daily enable row level security;

drop policy if exists profile_select on public.profile;
create policy profile_select on public.profile
  for select using (user_id = auth.uid());

drop policy if exists profile_insert on public.profile;
create policy profile_insert on public.profile
  for insert with check (user_id = auth.uid());

drop policy if exists device_select on public.device;
create policy device_select on public.device
  for select using (user_id = auth.uid());

drop policy if exists device_insert on public.device;
create policy device_insert on public.device
  for insert with check (user_id = auth.uid());

drop policy if exists review_event_select on public.review_event;
create policy review_event_select on public.review_event
  for select using (user_id = auth.uid());

drop policy if exists review_event_insert on public.review_event;
create policy review_event_insert on public.review_event
  for insert with check (user_id = auth.uid());

drop policy if exists user_content_select on public.user_content;
create policy user_content_select on public.user_content
  for select using (user_id = auth.uid());

drop policy if exists user_content_insert on public.user_content;
create policy user_content_insert on public.user_content
  for insert with check (user_id = auth.uid());

drop policy if exists settings_select on public.settings;
create policy settings_select on public.settings
  for select using (user_id = auth.uid());

drop policy if exists settings_insert on public.settings;
create policy settings_insert on public.settings
  for insert with check (user_id = auth.uid());

-- sync_cursor has no user_id column, so ownership is read through device.
drop policy if exists sync_cursor_select on public.sync_cursor;
create policy sync_cursor_select on public.sync_cursor
  for select using (
    device_id in (select d.device_id from public.device d where d.user_id = auth.uid())
  );

drop policy if exists sync_cursor_insert on public.sync_cursor;
create policy sync_cursor_insert on public.sync_cursor
  for insert with check (
    device_id in (select d.device_id from public.device d where d.user_id = auth.uid())
  );

-- analytics_daily takes writes and gives nothing back. There is no select
-- policy, so a signed-in client cannot read any row, its own included.
drop policy if exists analytics_daily_insert on public.analytics_daily;
create policy analytics_daily_insert on public.analytics_daily
  for insert with check (true);

-- ---------------------------------------------------------------------------
-- 3. The server assigns server_seq
-- ---------------------------------------------------------------------------
-- A client that writes its own server_seq can hide its events from its own next
-- pull, or push another device into re-reading everything. The insert policy
-- above cannot stop it, because the policy only checks user_id. This trigger
-- overwrites whatever the client sent. Test 9 of the plan proves it.

-- bigserial puts a default on the column, and the trigger below overwrites whatever
-- that default produced. Both call nextval, so each insert burned two numbers. Gaps do
-- no harm, because a pull asks for "events after N" and never assumes the numbers run
-- without holes (docs/07 section 5.4). Still, there is no reason to keep the waste.
-- Dropping the default leaves the trigger as the only writer.
alter table public.review_event alter column server_seq drop default;

create or replace function public.review_event_force_server_seq()
returns trigger
language plpgsql
as $fn$
begin
  new.server_seq := nextval('public.review_event_server_seq_seq');
  return new;
end;
$fn$;

drop trigger if exists review_event_force_server_seq on public.review_event;
create trigger review_event_force_server_seq
  before insert on public.review_event
  for each row execute function public.review_event_force_server_seq();

-- ---------------------------------------------------------------------------
-- 4. Grants
-- ---------------------------------------------------------------------------
-- RLS decides which rows. These grants decide which actions are offered at all.
-- Supabase grants new public tables to anon and authenticated by default; the
-- lines below make that explicit, and survive a project where the default was
-- changed.

revoke all on public.profile, public.device, public.review_event,
  public.user_content, public.settings, public.sync_cursor,
  public.analytics_daily from anon, authenticated;

grant select, insert on public.profile, public.device, public.review_event,
  public.user_content, public.settings, public.sync_cursor to authenticated;

grant insert on public.analytics_daily to authenticated;

-- The keep-alive ping reads one row as anon, through RLS, and gets zero rows
-- back. That is the point: it proves the public path answers, not that the
-- data is open.
grant select on public.review_event to anon;
