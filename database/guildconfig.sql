CREATE TABLE IF NOT EXISTS guild_config(
    guild_id bigint,
    welcomer boolean,
    welcomer_channel bigint,
    welcomer_msg character varying,
    on_join_role bigint,
    leaver boolean,
    leaver_channel bigint,
    leaver_msg character varying,
    leveller boolean,
    level_up_msg boolean,
    nqnf boolean,
    mod_logs boolean,
    mod_logs_channel bigint,
    server_updates boolean,
    server_updates_channel bigint,
    setup_channel bigint,
    PRIMARY KEY (guild_id)
);
