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

    select *
    into _user
    from users._ us
    where us.name = _login and us.hash = _password and us.deleted_at is null;

    user_id := _user.id;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        user_id := null;
        error := format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;