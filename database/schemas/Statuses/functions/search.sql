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
