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