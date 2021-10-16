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
