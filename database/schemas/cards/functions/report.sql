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

-- exception
--     when others then
--         get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
--         _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
--         raise
--             notice 'ERROR: % ', _exception;
--
--         return query with t as (
--             values (errors.exception(_exception),
--                     null::uuid,
--                     null::uuid,
--                     null::timestamptz,
--                     null::varchar,
--                     null::varchar,
--                     null::varchar,
--                     null::jsonb))
--                      select *
--                      from t;
end ;
$$
    language plpgsql stable
                     security definer;
--
-- alter function users.search(
--     _invoker_id uuid,
--     _sort_field varchar,
--     _sort_order int,
--     _page int,
--     _page_size int,
--     _locale_id varchar,
--     _time_zone_id varchar,
--     _display_name varchar,
--     _role_id uuid,
--     --
--     out error jsonb,
--     out user_id uuid,
--     out creator_id uuid,
--     out created_at timestamptz,
--     out locale_id varchar,
--     out time_zone_id varchar,
--     out display_name varchar,
--     out payload jsonb
--     ) owner to postgres;
--
-- grant execute on function users.search(
--     _invoker_id uuid,
--     _sort_field varchar,
--     _sort_order int,
--     _page int,
--     _page_size int,
--     _locale_id varchar,
--     _time_zone_id varchar,
--     _display_name varchar,
--     _role_id uuid,
--     --
--     out error jsonb,
--     out user_id uuid,
--     out creator_id uuid,
--     out created_at timestamptz,
--     out locale_id varchar,
--     out time_zone_id varchar,
--     out display_name varchar,
--     out payload jsonb
--     ) to postgres, web;
--
-- revoke all on function users.search(
--     _invoker_id uuid,
--     _sort_field varchar,
--     _sort_order int,
--     _page int,
--     _page_size int,
--     _locale_id varchar,
--     _time_zone_id varchar,
--     _display_name varchar,
--     _role_id uuid,
--     --
--     out error jsonb,
--     out user_id uuid,
--     out creator_id uuid,
--     out created_at timestamptz,
--     out locale_id varchar,
--     out time_zone_id varchar,
--     out display_name varchar,
--     out payload jsonb
--     ) from public;