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

        error := format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception);
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