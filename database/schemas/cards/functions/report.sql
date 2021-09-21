create or replace function cards.report(
    _board_id uuid = null,
    _status_id uuid = null,
    _priority_id uuid = null,
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

        return query with err as
                              (values  (error::jsonb,
                                        null::varchar,
                                        null::varchar,
                                        null::uuid,
                                        null::varchar,
                                        null::varchar,
                                        null::integer,
                                        null::uuid,
                                        null::uuid,
                                        null::timestamptz,
                                        null::timestamptz))
                              select *
                              from err;
        return;
    end if;

    if _status_id is not null
        and not exists(select 1
                       from statuses._
                       where id = _status_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_status_id"}';

        return query with err as
                              (values  (error::jsonb,
                                        null::varchar,
                                        null::varchar,
                                        null::uuid,
                                        null::varchar,
                                        null::varchar,
                                        null::integer,
                                        null::uuid,
                                        null::uuid,
                                        null::timestamptz,
                                        null::timestamptz))
                              select *
                              from err;
        return;
    end if;

    if _priority_id is not null
        and not exists(select 1
                       from priorities._
                       where id = _priority_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_priority_id"}';

        return query with err as
                              (values  (error::jsonb,
                                        null::varchar,
                                        null::varchar,
                                        null::uuid,
                                        null::varchar,
                                        null::varchar,
                                        null::integer,
                                        null::uuid,
                                        null::uuid,
                                        null::timestamptz,
                                        null::timestamptz))
                              select *
                              from err;
        return;
    end if;


    if _developer_id is not null
        and not exists(select 1
                       from users._
                       where id = _developer_id)
    then
        error := '{"code": 1, "reason": "not_found", "description": "_developer_id"}';

        return query with err as
                              (values  (error::jsonb,
                                        null::varchar,
                                        null::varchar,
                                        null::uuid,
                                        null::varchar,
                                        null::varchar,
                                        null::integer,
                                        null::uuid,
                                        null::uuid,
                                        null::timestamptz,
                                        null::timestamptz))
                              select *
                              from err;
        return;
    end if;

    return query (
        with tab as (
            select null::jsonb                                                 as error,
                   c.title                                                     as title,
                   c.description                                               as description,
                   c.developer_id                                              as developer_id,
                   (select _.title from priorities._ where id = c.priority_id) as priority,
                   (select _.title from statuses._ where id = c.status_id)     as status,
                   c.estimates_time                                            as estimates_time,
                   c.board_id                                                  as board_id,
                   c.creator_id                                                as creator_id,
                   c.created_at                                                as created_at,
                   c.updated_at                                                as updated_at
            from cards._ c
            where c.deleted_at is null
              and (
                    _board_id is null
                    or c.board_id = _board_id
                )
              and (
                    _status_id is null
                    or c.status_id = _status_id
                )
              and (
                    _priority_id is null
                    or c.priority_id = _priority_id
                )
              and (
                    _developer_id is null
                    or c.developer_id = _developer_id
                )
        )
        select     null::jsonb       as error,
                   c.title           as title,
                   c.description     as description,
                   c.developer_id    as developer_id,
                   c.priority        as priority,
                   c.status          as status,
                   c.estimates_time  as estimates_time,
                   c.board_id        as board_id,
                   c.creator_id      as creator_id,
                   c.created_at      as created_at,
                   c.updated_at      as updated_at
        from tab as c);


exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query with t as (
            values (format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception)::jsonb,
                    null::varchar,
                    null::varchar,
                    null::uuid,
                    null::varchar,
                    null::varchar,
                    null::integer,
                    null::uuid,
                    null::uuid,
                    null::timestamptz,
                    null::timestamptz))
                     select *
                     from t;
end ;
$$
    language plpgsql stable
                     security definer;

alter function cards.report(
    _board_id uuid,
    _status_id uuid,
    _priority_id uuid,
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
    _board_id uuid,
    _status_id uuid,
    _priority_id uuid,
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
    _board_id uuid,
    _status_id uuid,
    _priority_id uuid,
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
