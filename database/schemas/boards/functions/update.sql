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