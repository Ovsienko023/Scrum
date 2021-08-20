create or replace function users.create(
    _name varchar,
    _hash text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _name := nullif(trim(_name), '');

    if _name is null then
        error := '{"errors": "_name"}';
        return;
    end if;

    if exists(select 1
              from users.users
              where name = _name)
    then
        error := '{"errors": "_name"}';
        return;
    end if;

    _hash := nullif(trim(_hash), '');

    if _hash is null then
        error := '{"errors": "_hash"}';
        return;
    end if;

    if exists(select 1
              from users.users
              where hash = _hash)
    then
        error := '{"errors": "_hash"}';
        return;
    end if;

    insert into users.users as u (name, hash)
    values (_name, _hash)
    returning u.id, u.created_at into user_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        user_id := null;
        created_at := null;
        error := '{"errors": "unknown"}';
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function users.create(
    _name varchar,
    _hash text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function users.create(
    _name varchar,
    _hash text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function users.create(
    _name varchar,
    _hash text,
    --
    out error jsonb,
    out user_id uuid,
    out created_at timestamptz
    ) from public;
