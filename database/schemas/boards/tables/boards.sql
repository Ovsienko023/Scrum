create table if not exists boards._
(
    id         uuid     primary key  default gen_random_uuid(),
    title      varchar  not null,
    creator_id uuid     references   users._ (id),
    created_at timestamptz not null default now(),
    deleted_at timestamptz
);
