create table if not exists cards._
(
    id             bigserial    primary key,
    title          varchar      not null,
    description    varchar,
    developer_id   uuid         references   users._ (id),
    priority_id    uuid         references   priorities._ (id),
    status_id      uuid         references   statuses._ (id),
    board_id       uuid         references   boards._ (id),
    creator_id     uuid         references   users._ (id),
    estimates_time int          not null,
    created_at     timestamptz  not null     default now(),
    updated_at     timestamptz  not null     default now(),
    deleted_at     timestamptz
);
