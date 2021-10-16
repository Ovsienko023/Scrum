create table if not exists users._
(
    id             uuid primary key     default gen_random_uuid(),
    created_at     timestamptz not null default now(),
    display_name   varchar     not null,
    login          varchar     not null,
    hash           text        not null,
    deleted_at timestamptz
);

insert into users._ (display_name, login, hash) values ('Admin', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');
