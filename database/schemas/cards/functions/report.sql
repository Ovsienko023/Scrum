create or replace function cards.report(
    _board_id     uuid = null,
    _status       varchar = null,
    _priority     varchar = null,
    _developer_id uuid = null,
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
    out created_at timestamptz,
    out updated_at timestamptz
) returns setof record as
$$
declare
    _exception     text;
begin

    if _board_id is not null
        and not exists(select 1
                       from boards._
                       where id = _board_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_board_id"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    if _status is not null
        and not exists(select 1
                       from statuses._ st
                       where st.title = _status)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_status"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    if _priority is not null
        and not exists(select 1
                       from priorities._ pr
                       where pr.title = _priority)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_priority"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;


    if _developer_id is not null
        and not exists(select 1
                       from users._
                       where id = _developer_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_developer_id"}';

        return query
            values( error::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
        return;
    end if;

    return query (select null::jsonb   as error,
                   c.title             as title,
                   c.description       as description,
                   c.developer_id      as developer_id,
                   c.priority          as priority,
                   c.status            as status,
                   c.estimates_time    as estimates_time,
                   c.board_id          as board_id,
                   c.creator_id        as creator_id,
                   c.created_at        as created_at,
                   c.updated_at        as updated_at
            from cards._ c
            where c.deleted_at is null
              and (
                    _board_id is null
                    or c.board_id = _board_id
                )
              and (
                    _status is null
                    or c.status = _status
                )
              and (
                    _priority is null
                    or c.priority = _priority
                )
              and (
                    _developer_id is null
                    or c.developer_id = _developer_id
                )
        );
    return;

exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query
            values (format('{"code": -1, "reason": "unknown", "description": "%s"}',_exception)::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz);
end ;
$$
    language plpgsql stable
                     security definer;

alter function cards.report(
    _board_id     uuid,
    _status_id    varchar,
    _priority_id  varchar,
    _developer_id uuid,
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
    out created_at timestamptz,
    out updated_at timestamptz
    ) owner to postgres;

grant execute on function cards.report(
    _board_id     uuid,
    _status       varchar,
    _priority     varchar,
    _developer_id uuid,
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
    out created_at timestamptz,
    out updated_at timestamptz
    ) to postgres;

revoke all on function cards.report(
    _board_id     uuid,
    _status       varchar,
    _priority     varchar,
    _developer_id uuid,
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
    out created_at timestamptz,
    out updated_at timestamptz
    ) from public;
