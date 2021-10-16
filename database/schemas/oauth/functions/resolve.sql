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
