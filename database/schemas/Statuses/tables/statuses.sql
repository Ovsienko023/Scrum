create table if not exists statuses._
(
    title varchar   primary key
);

insert into statuses._ (title)
values ('New'),
       ('In development'),
       ('Developed'),
       ('On hold'),
       ('Closed')

on conflict do nothing;
