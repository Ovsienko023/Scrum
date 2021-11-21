-- create database postgres;
CREATE EXTENSION pgcrypto;
 
create schema users;
 
create or replace function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error      jsonb,
    out user_id    uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _display_name := nullif(trim(_display_name), '');

    if _display_name is null then
        error := '{"code": 2, "reason": "required", "description": "_display_name"}';
        return;
    end if;

    _login := nullif(trim(_login), '');
    if _login is null then
        error := '{"code": 2, "reason": "required", "description": "_login"}';
        return;
    end if;

    if exists(select 1
              from users._
              where login = _login)
    then
        error := '{"code": 3, "reason": "exists", "description": "_login"}';
        return;
    end if;

    _hash := nullif(trim(_hash), '');

    if _hash is null then
        error := '{"code": 2, "reason": "required", "description": "_hash"}';
        return;
    end if;

    insert into users._ as u (display_name, login, hash)
    values (_display_name, _login, _hash)
    returning u.id, u.created_at into user_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        user_id := null;
        created_at := null;
        error := '{"code": -1, "reason": "unknown", "description": "%"}',_exception;
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) from public;

 

 

 

 
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

 
create schema oauth;
 
create or replace function oauth.get_token(
    _login varchar,
    _password varchar,
    --
    out error jsonb,
    out user_id uuid
) as
$$
declare
    _user       record;
    _exception  text;
begin

    _login := nullif(trim(_login), '');
    if _login is null then
        error := '{"code": 2, "reason": "required", "description": "_login"}';
        return;
    end if;

    if not exists(select 1
                  from users._ u
                  where u.login = _login)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_login"}';
        return;
    end if;

    _password := nullif(trim(_password), '');
    if _password is null then
        error := '{"code": 2, "reason": "required", "description": "_password"}';
        return;
    end if;
    if not exists(select 1
                  from users._ u
                  where u.login = _login and u.hash = _password)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_password"}';
        return;
    end if;

    select *
    into _user
    from users._ us
    where us.login = _login and us.hash = _password and us.deleted_at is null;

    user_id := _user.id;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        user_id := null;
        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function oauth.get_token(
    _login varchar,
    _password varchar,
    --
    out error jsonb,
    out user_id uuid
    ) owner to postgres;

grant execute on function oauth.get_token(
    _login varchar,
    _password varchar,
    --
    out error jsonb,
    out user_id uuid
    ) to postgres;

revoke all on function oauth.get_token(
    _login varchar,
    _password varchar,
    --
    out error jsonb,
    out user_id uuid
    ) from public;

 
create or replace function oauth.resolve(
    _user_id uuid,
    --
    out error jsonb
) as
$$
declare
    _exception  text;
begin

    if not exists(select 1
                  from users._ u
                  where u.id = _user_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_user_id"}';
        return;
    end if;


exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function oauth.resolve(
    _user_id uuid,
    --
    out error jsonb
    ) owner to postgres;

grant execute on function oauth.resolve(
    _user_id uuid,
    --
    out error jsonb
    ) to postgres;

revoke all on function oauth.resolve(
    _user_id uuid,
    --
    out error jsonb
    ) from public;

 
create schema priorities;
 
create or replace function priorities.search(
    --
    out error jsonb,
    out title varchar
) returns setof record as
$$
declare
    _exception     text;
begin

    return query (select   null::jsonb       as error,
                           p.title           as title
                  from priorities._ p);
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query
            values (format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception)::jsonb,
                    null::varchar);
        return;
end ;
$$
    language plpgsql stable
                     security definer;

alter function priorities.search(
    --
    out error jsonb,
    out title varchar
    ) owner to postgres;

grant execute on function priorities.search(
    --
    out error jsonb,
    out title varchar
    ) to postgres;

revoke all on function priorities.search(
    --
    out error jsonb,
    out title varchar
    ) from public;

 
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

 
create schema statuses;
 
create or replace function statuses.search(
    --
    out error jsonb,
    out title varchar
) returns setof record as
$$
declare
    _exception     text;
begin

    return query (select   null::jsonb       as error,
                           s.title           as title
                  from statuses._ s);
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query
            values (format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception)::jsonb,
                    null::varchar);
        return;
end ;
$$
    language plpgsql stable
                     security definer;

alter function statuses.search(
    --
    out error jsonb,
    out title varchar
    ) owner to postgres;

grant execute on function statuses.search(
    --
    out error jsonb,
    out title varchar
    ) to postgres;

revoke all on function statuses.search(
    --
    out error jsonb,
    out title varchar
    ) from public;

 
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

 
create schema boards;
 
create or replace function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _title := nullif(trim(_title), '');

    if _title is null then
        error := '{"code": 2, "reason": "required", "description": "_title"}';
        return;
    end if;

    if exists(select 1
              from boards._
              where title = _title)
    then
        error := '{"code": 3, "reason": "exists", "description": "_title"}';
        return;
    end if;

    if not exists(select 1
              from users._
              where id = _creator_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_creator_id"}';
        return;
    end if;

    insert into boards._ as b (title, creator_id)
    values (_title, _creator_id)
    returning b.id, b.created_at into board_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        board_id := null;
        created_at := null;
        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) from public;

 
create or replace function boards.delete(
    _board_id  uuid,
    --
    out error  jsonb
) as
$$

declare
    _exception     text;
begin

    if not exists(select id
                  from boards._ as b
                  where b.id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    update boards._
    set deleted_at          = now()
    where id = _board_id;

    error := null;
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.delete(
    _board_id       uuid,
    --
    out error jsonb
    ) owner to postgres;

grant execute on function boards.delete(
    _board_id       uuid,
    --
    out error jsonb
    ) to postgres;

revoke all on function boards.delete(
    _board_id       uuid,
    --
    out error jsonb
    ) from public;
 
create or replace function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    if _board_id is null then
        error := '{"code": 2, "reason": "required", "description": "_board_id"}';
        return;
    end if;

    if not exists(select 1
              from boards._
              where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    select b.title,
           b.created_at,
           b.creator_id
    into
        get.title,
        get.created_at,
        get.creator_id
    from boards._ as b
    where b.id = _board_id
      and b.deleted_at is null;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        title := null;
        created_at := null;
        creator_id := null;
        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) from public;

 
create or replace function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
) returns setof record as
$$
declare
    _exception     text;
begin

    return query (select
                       null::jsonb       as error,
                       b.id              as board_id,
                       b.title           as title,
                       b.creator_id      as creator_id,
                       b.created_at      as created_at
                    from boards._ b
                    where b.deleted_at is null);
    return;


exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query
            values (format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception)::jsonb,
                    null::uuid,
                    null::varchar,
                    null::uuid,
                    null::timestamptz);
        return;
end ;
$$
    language plpgsql stable
                     security definer;

alter function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) from public;

 
create or replace function boards.update(
    _board_id  uuid,
    _title     varchar = null,
    --
    out error  jsonb
) as
$$

declare
    _exception     text;
begin

    if not exists(select id
                  from boards._ as b
                  where b.id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    if _title is null
    then
        error := '{"code": 5, "reason": "not_found", "description": "fields"}';
        return;
    end if;

    _title := nullif(trim(_title), '');

    update boards._
    set title          = coalesce(_title, title)
    where id = _board_id
      and deleted_at is null;

    error := null;
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.update(
    _board_id       uuid,
    _title          varchar,
    --
    out error jsonb
    ) owner to postgres;

grant execute on function boards.update(
    _board_id       uuid,
    _title          varchar,
    --
    out error jsonb
    ) to postgres;

revoke all on function boards.update(
    _board_id       uuid,
    _title          varchar,
    --
    out error jsonb
    ) from public;
 
create table if not exists boards._
(
    id         uuid     primary key  default gen_random_uuid(),
    title      varchar  not null,
    creator_id uuid     references   users._ (id),
    created_at timestamptz not null default now(),
    deleted_at timestamptz
);

 
create schema cards;
 
create or replace function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _title := nullif(trim(_title), '');
    _description := nullif(trim(_description), '');

    if _title is null then
        error := '{"code": 2, "reason": "required", "description": "_title"}';
        return;
    end if;

    if _description is null then
        error := '{"code": 2, "reason": "required", "description": "_description"}';
        return;
    end if;

    if not exists(select 1
              from users._
              where id = _developer_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_developer_id"}';
        return;
    end if;

    if not exists(select 1
              from priorities._
              where title = _priority)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_priority"}';
        return;
    end if;

    if not exists(select 1
              from boards._
              where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    if not exists(select 1
              from users._
              where id = _creator_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_creator_id"}';
        return;
    end if;

    if _estimates_time <= 0
    then
        error := '{"code": 4, "reason": "validate", "description": "_estimates_time"}';
        return;
    end if;

    insert into cards._ as c (title, description, developer_id, priority, status, board_id, creator_id, estimates_time, deleted_at)
    values (_title, _description, _developer_id, _priority, 'New', _board_id, _creator_id, _estimates_time, null)
    returning c.id, c.created_at into card_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        card_id := null;
        created_at := null;
        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) to postgres;

revoke all on function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) from public;

 
create or replace function cards.delete(
    _card_id  bigint,
    --
    out error  jsonb
) as
$$

declare
    _exception     text;
begin

    if not exists(select id
                  from cards._ as c
                  where c.id = _card_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_card_id"}';
        return;
    end if;

    update cards._
    set deleted_at       = now()
    where id = _card_id;

    error := null;
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.delete(
    _card_id   bigint,
    --
    out error jsonb
    ) owner to postgres;

grant execute on function cards.delete(
    _card_id   bigint,
    --
    out error jsonb
    ) to postgres;

revoke all on function cards.delete(
    _card_id   bigint,
    --
    out error jsonb
    ) from public;
 
create or replace function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
) as
$$
declare
    _exception     text;
begin
    if _card_id is null then
        error := '{"code": 2, "reason": "required", "description": "_card_id"}';
        return;
    end if;

    if not exists(select 1
              from cards._
              where id = _card_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_card_id"}';
        return;
    end if;

    select c.title,
           c.description,
           c.developer_id,
           c.priority,
           c.status,
           c.estimates_time,
           c.board_id,
           c.creator_id,
           c.created_at,
           c.updated_at
    into
        get.title,
        get.description,
        get.developer_id,
        get.priority,
        get.status,
        get.estimates_time,
        get.board_id,
        get.creator_id,
        get.created_at,
        get.updated_at

    from cards._ as c
    where c.id = _card_id
      and c.deleted_at is null;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        title := null;
        description := null;
        developer_id := null;
        priority := null;
        status := null;
        estimates_time := null;
        board_id := null;
        creator_id := null;
        created_at := null;
        updated_at := null;
        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) owner to postgres;

grant execute on function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) to postgres;

revoke all on function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) from public;

 
create or replace function cards.report(
    _board_id     uuid = null,
    _status       varchar = null,
    _priority     varchar = null,
    _developer_id uuid = null,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
) returns setof record as
$$
declare
    _exception     text;
begin

    if _board_id is not null
        and not exists(select 1
                       from boards._
                       where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    if _status is not null
        and not exists(select 1
                       from statuses._ st
                       where st.title = _status)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_status"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    if _priority is not null
        and not exists(select 1
                       from priorities._ pr
                       where pr.title = _priority)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_priority"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;


    if _developer_id is not null
        and not exists(select 1
                       from users._
                       where id = _developer_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_developer_id"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    return query (select null::jsonb   as error,
                   c.title             as title,
                   c.description       as description,
                   c.developer_id      as developer_id,
                   c.priority          as priority,
                   c.status            as status,
                   c.estimates_time    as estimates_time,
                   c.board_id          as board_id,
                   c.creator_id        as creator_id,
                   c.created_at        as created_at,
                   c.updated_at        as updated_at
            from cards._ c
            where c.deleted_at is null
              and (
                    _board_id is null
                    or c.board_id = _board_id
                )
              and (
                    _status is null
                    or c.status = _status
                )
              and (
                    _priority is null
                    or c.priority = _priority
                )
              and (
                    _developer_id is null
                    or c.developer_id = _developer_id
                )
        );
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query
            values (format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception)::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
end ;
$$
    language plpgsql stable
                     security definer;

alter function cards.report(
    _board_id     uuid,
    _status_id    varchar,
    _priority_id  varchar,
    _developer_id uuid,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) owner to postgres;

grant execute on function cards.report(
    _board_id     uuid,
    _status       varchar,
    _priority     varchar,
    _developer_id uuid,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) to postgres;

revoke all on function cards.report(
    _board_id     uuid,
    _status       varchar,
    _priority     varchar,
    _developer_id uuid,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz,
    out updated_at timestamptz
    ) from public;

 
create or replace function cards.update(
    _card_id        bigint,
    _title          varchar = null,
    _description    varchar = null,
    _developer_id   uuid = null,
    _priority       varchar = null,
    _status         varchar = null,
    _board_id       uuid = null,
    _estimates_time int = null,
    --
    out error jsonb
) as
$$

declare
    _exception     text;
begin

    if not exists(select id
                  from cards._ as c
                  where c.id = _card_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_card_id"}';
        return;
    end if;

    if _title is null and
    _description is null and
    _developer_id is null and
    _priority  is null and
    _status  is null and
    _board_id is null and
    _estimates_time is null
    then
        error := '{"code": 5, "reason": "not_found", "description": "fields"}';
        return;
    end if;

    _title := nullif(trim(_title), '');
    _description := nullif(trim(_description), '');
    _priority := nullif(trim(_priority), '');
    _status := nullif(trim(_status), '');

    if _developer_id is not null and
        not exists(select 1
          from users._
          where id = _developer_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_developer_id"}';
        return;
    end if;

    if _priority is not null and
       not exists(select 1
          from priorities._
          where title = _priority)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_priority"}';
        return;
    end if;

    if _status is not null and
       not exists(select 1
          from statuses._
          where title = _status)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_status"}';
        return;
    end if;

    if _board_id is not null and
       not exists(select 1
              from boards._
              where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    if _estimates_time is not null and _estimates_time <= 0
    then
        error := '{"code": 4, "reason": "validate", "description": "_estimates_time"}';
        return;
    end if;

    update cards._
    set title          = coalesce(_title, title),
        description    = coalesce(_description, description),
        developer_id   = coalesce(_developer_id, developer_id),
        priority       = coalesce(_priority, priority),
        status         = coalesce(_status, status),
        board_id       = coalesce(_board_id, board_id),
        estimates_time = coalesce(_estimates_time, estimates_time),
        updated_at     = now()
    where id = _card_id
      and deleted_at is null;

    error := null;
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        error := format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.update(
    _card_id        bigint,
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _status         varchar,
    _board_id       uuid,
    _estimates_time int,
    --
    out error jsonb
    ) owner to postgres;

grant execute on function cards.update(
    _card_id        bigint,
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _status         varchar,
    _board_id       uuid,
    _estimates_time int,
    --
    out error jsonb
    ) to postgres;

revoke all on function cards.update(
    _card_id        bigint,
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority       varchar,
    _status         varchar,
    _board_id       uuid,
    _estimates_time int,
    --
    out error jsonb
    ) from public;
 
create table if not exists cards._
(
    id             bigserial    primary key,
    title          varchar      not null,
    description    varchar,
    developer_id   uuid         references   users._ (id),
    priority       varchar      references   priorities._ (title),
    status         varchar      references   statuses._ (title),
    board_id       uuid         references   boards._ (id),
    creator_id     uuid         references   users._ (id),
    estimates_time int          not null,
    created_at     timestamptz  not null     default now(),
    updated_at     timestamptz  not null     default now(),
    deleted_at     timestamptz
);

 
