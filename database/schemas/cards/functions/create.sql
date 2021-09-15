create or replace function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority_id    uuid,
    _status_id      uuid,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin
    _title := nullif(trim(_title), '');
    _description := nullif(trim(_description), '');

    if _title is null then
        error := '{"errors": {"code": 2, "reason": "required", "description": "_title"}}';
        return;
    end if;
    if exists(select 1
              from cards._
              where title = _title)
    then
        error := '{"errors": {"code": 3, "reason": "exists", "description": "_title"}}';
        return;
    end if;

    if _description is null then
        error := '{"errors": {"code": 2, "reason": "required", "description": "_description"}}';
        return;
    end if;
    if exists(select 1
              from cards._
              where title = _description)
    then
        error := '{"errors": {"code": 3, "reason": "exists", "description": "_description"}}';
        return;
    end if;

    if not exists(select 1
              from users._
              where id = _developer_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_developer_id"}}';
        return;
    end if;

    if not exists(select 1
              from priorities._
              where id = _priority_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_priority_id"}}';
        return;
    end if;

    if not exists(select 1
              from statuses._
              where id = _status_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_status_id"}}';
        return;
    end if;

    if not exists(select 1
              from boards._
              where id = _board_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_board_id"}}';
        return;
    end if;

    if not exists(select 1
              from users._
              where id = _creator_id)
    then
        error := '{"errors": {"code": 1, "reason": "not_found", "description": "_creator_id"}}';
        return;
    end if;

    if _estimates_time <= 0
    then
        error := '{"errors": {"code": 4, "reason": "validate", "description": "_estimates_time"}}';
        return;
    end if;

    insert into cards._ as c (title, description, developer_id, priority_id, status_id, board_id, creator_id, estimates_time, deleted_at)
    values (_title, _description, _developer_id, _priority_id, _status_id, _board_id, _creator_id, _estimates_time, null)
    returning c.id, c.created_at into card_id, created_at;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception := _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise notice 'ERROR: % ', _exception;

        card_id := null;
        created_at := null;
        error := '{"errors": {"code": -1, "reason": "unknown", "description": "%"}}',_exception;
        return;

end;
$$
    language plpgsql volatile
                     security definer;

alter function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority_id    uuid,
    _status_id      uuid,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority_id    uuid,
    _status_id      uuid,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) to postgres;

revoke all on function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority_id    uuid,
    _status_id      uuid,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    --
    out error jsonb,
    out card_id bigint,
    out created_at timestamptz
    ) from public;
