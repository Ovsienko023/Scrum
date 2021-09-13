create or replace function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _title := nullif(trim(_title), '');

    if _title is null then
        error := '{"errors": {"code": 2, "reason": "required", "description": "_title"}}';
        return;
    end if;

    if exists(select 1
              from boards._
              where title = _title)
    then
        error := '{"errors": {"code": 3, "reason": "exists", "description": "_title"}}';
        return;
    end if;

--     _creator_id := nullif(trim(_creator_id), '');

    if not exists(select 1
              from users._
              where id = _creator_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_creator_id"}}';
        return;
    end if;

    insert into boards._ as b (title, creator_id)
    values (_title, _creator_id)
    returning b.id, b.created_at into board_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        board_id := null;
        created_at := null;
        error := '{"errors": {"code": -1, "reason": "unknown", "description": "%"}}',_exception;
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.create(
    _title varchar,
    _creator_id uuid,
    --
    out error jsonb,
    out board_id uuid,
    out created_at timestamptz
    ) from public;
