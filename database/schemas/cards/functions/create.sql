create or replace function cards.create(
    _title          varchar,
    _description    varchar,
    _developer_id   uuid,
    _priority_id    uuid,
    _status_id      uuid,
    _board_id       uuid,
    _creator_id     uuid,
    _estimates_time int,
    _created_at     timestamptz,
    --
    out error jsonb,
    out card_id uuid,
    out created_at timestamptz
) as
$$
declare
    _exception     text;
begin

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
    _created_at     timestamptz,
    --
    out error jsonb,
    out card_id uuid,
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
    _created_at     timestamptz,
    --
    out error jsonb,
    out card_id uuid,
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
    _created_at     timestamptz,
    --
    out error jsonb,
    out card_id uuid,
    out created_at timestamptz
    ) from public;
