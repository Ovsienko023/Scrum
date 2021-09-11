create table if not exists priorities._
(
    id       uuid primary key     default gen_random_uuid(),
    title    varchar not null
);

insert into priorities._ (title)
values ('Low'),
       ('Normal'),
       ('High'),
       ('Immediate')

on conflict do nothing;
