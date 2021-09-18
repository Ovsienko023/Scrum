create or replace function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    if _card_id is null then
        error := '{"code": 2, "reason": "required", "description": "_card_id"}';
        return;
    end if;

    if not exists(select 1
              from cards._
              where id = _card_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_card_id"}';
        return;
    end if;

    select c.title,
           c.description,
           c.developer_id,
           (select _.title
            from priorities._
                where id = c.priority_id),
           (select _.title
            from statuses._
                where id = c.status_id),
           c.estimates_time,
           c.board_id,
           c.creator_id,
           c.created_at
    into
        get.title,
        get.description,
        get.developer_id,
        get.priority,
        get.status,
        get.estimates_time,
        get.board_id,
        get.creator_id,
        get.created_at

    from cards._ as c
    where c.id = _card_id
      and c.deleted_at is null;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        title := null;
        description := null;
        developer_id := null;
        priority := null;
        status := null;
        estimates_time := null;
        board_id := null;
        creator_id := null;
        created_at := null;
        error := format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception);
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function cards.get(
    _card_id bigint,
    --
    out error jsonb,
    out title varchar,
    out description varchar,
    out developer_id uuid,
    out priority varchar,
    out status varchar,
    out estimates_time integer,
    out board_id uuid,
    out creator_id uuid,
    out created_at timestamptz
    ) from public;
