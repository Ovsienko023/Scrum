create table if not exists users.users
(
    id         uuid primary key     default gen_random_uuid(),
    created_at timestamptz not null default now(),
    name       varchar     not null,
    hash       text        not null,
    deleted_at timestamptz
);

insert into users.users (name, hash) values ('admin', 'qwerty');
