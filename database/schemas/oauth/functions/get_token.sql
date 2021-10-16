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
