create table if not exists priorities._
(
    title varchar  primary key
);

insert into priorities._ (title)
values ('Low'),
       ('Normal'),
       ('High'),
       ('Immediate')

on conflict do nothing;
