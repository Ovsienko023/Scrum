create or replace function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    if _board_id is null then
        error := '{"code": 2, "reason": "required", "description": "_board_id"}';
        return;
    end if;

    if not exists(select 1
              from boards._
              where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';
        return;
    end if;

    select b.title,
           b.created_at,
           b.creator_id
    into
        get.title,
        get.created_at,
        get.creator_id
    from boards._ as b
    where b.id = _board_id
      and b.deleted_at is null;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        title := null;
        created_at := null;
        creator_id := null;
        error := '{"errors": {"code": -1, "reason": "unknown", "description": "%"}}',_exception;
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.get(
    _board_id uuid,
    --
    out error jsonb,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) from public;
