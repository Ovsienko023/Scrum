create or replace function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
) returns setof record as
$$
declare
    _exception     text;
begin

    return query (
        with tab as (
                    select     null::jsonb       as error,
                               b.id              as board_id,
                               b.title           as title,
                               b.creator_id      as creator_id,
                               b.created_at      as created_at
            from boards._ b
            where b.deleted_at is null
        )
        select     null::jsonb       as error,
                   b.board_id        as board_id,
                   b.title           as title,
                   b.creator_id      as creator_id,
                   b.created_at      as created_at
        from tab as b);


exception
    when others then
        get stacked diagnostics _exception = PG_EXCEPTION_CONTEXT;
        _exception = _exception || ' | ' || SQLERRM || ' | ' || SQLSTATE;
        raise
            notice 'ERROR: % ', _exception;

        return query with t as (
            values (format('{"errors": {"code": -1, "reason": "unknown", "description": "%s"}}',_exception)::jsonb,
                    null::uuid,
                    null::varchar,
                    null::uuid,
                    null::timestamptz))
                     select *
                     from t;
end ;
$$
    language plpgsql stable
                     security definer;

alter function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) owner to postgres;

grant execute on function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) to postgres;

revoke all on function boards.search(
    --
    out error jsonb,
    out board_id uuid,
    out title varchar,
    out creator_id uuid,
    out created_at timestamptz
    ) from public;
