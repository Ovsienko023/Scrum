create or replace function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error      jsonb,
    out user_id    uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _display_name := nullif(trim(_display_name), '');

    if _display_name is null then
        error := '{"code": 2, "reason": "required", "description": "_display_name"}';
        return;
    end if;

    _login := nullif(trim(_login), '');
    if _login is null then
        error := '{"code": 2, "reason": "required", "description": "_login"}';
        return;
    end if;

    if exists(select 1
              from users._
              where login = _login)
    then
        error := '{"code": 3, "reason": "exists", "description": "_login"}';
        return;
    end if;

    _hash := nullif(trim(_hash), '');

    if _hash is null then
        error := '{"code": 2, "reason": "required", "description": "_hash"}';
        return;
    end if;

    insert into users._ as u (display_name, login, hash)
    values (_display_name, _login, _hash)
    returning u.id, u.created_at into user_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        user_id := null;
        created_at := null;
        error := '{"code": -1, "reason": "unknown", "description": "%"}',_exception;
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function users.create(
    _display_name  varchar,
    _login         varchar,
    _hash          text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) from public;
