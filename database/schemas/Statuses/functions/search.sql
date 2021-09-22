create or replace function statuses.search(
    --
    out error jsonb,
    out status_id uuid,
    out title varchar
) returns setof record as
$$
declare
    _exception     text;
begin

    return query (select   null::jsonb       as error,
                           s.id              as status_id,
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
            values (format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception)::jsonb,
                    null::uuid,
                    null::varchar);
        return;
end ;
$$
    language plpgsql stable
                     security definer;

alter function statuses.search(
    --
    out error jsonb,
    out status_id uuid,
    out title varchar
    ) owner to postgres;

grant execute on function statuses.search(
    --
    out error jsonb,
    out status_id uuid,
    out title varchar
    ) to postgres;

revoke all on function statuses.search(
    --
    out error jsonb,
    out status_id uuid,
    out title varchar
    ) from public;