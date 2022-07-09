CREATE TABLE IF NOT EXISTS playerData (
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,

    SPEAK_COOLDOWN float DEFAULT CURRENT_TIMESTAMP,
    SCAVENGE_COOLDOWN float DEFAULT CURRENT_TIMESTAMP,

    SPOKE_DAY integer DEFAULT 0,
    SPOKEN_TO_DAY integer DEFAULT 0,

    QUOTE text DEFAULT 'I am not a bot, I am a human'
);

CREATE TABLE IF NOT EXISTS guilds (
    GuildID integer PRIMARY KEY,
    Prefix1 text DEFAULT 'a!',
    Prefix2 text DEFAULT 'none',
    Prefix3 text DEFAULT 'none',
    Prefix4 text DEFAULT 'none',
    Prefix5 text DEFAULT 'none'
);