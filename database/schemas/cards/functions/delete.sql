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