create table if not exists statuses.statuses
(
    id         uuid primary key     default gen_random_uuid(),
    title      varchar not null
);

insert into statuses.statuses (title)
values ('New'),
       ('In development'),
       ('Developed'),
       ('On hold'),
       ('Closed')

on conflict do nothing;
