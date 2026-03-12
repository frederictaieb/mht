CREATE TABLE IF NOT EXISTS actress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS avatar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    actress_id INTEGER NOT NULL,
    FOREIGN KEY (actress_id) REFERENCES actress(id)
);

CREATE TABLE IF NOT EXISTS scene (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scene_number INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS scene_presence (
    scene_id INTEGER NOT NULL,
    avatar_id INTEGER NOT NULL,
    PRIMARY KEY (scene_id, avatar_id),
    FOREIGN KEY (scene_id) REFERENCES scene(id) ON DELETE CASCADE,
    FOREIGN KEY (avatar_id) REFERENCES avatar(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS voice_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    avatar_id INTEGER NOT NULL,
    audio_reference_path TEXT NOT NULL,
    note TEXT,
    prompt_voice_clone_json TEXT NOT NULL,
    FOREIGN KEY (avatar_id) REFERENCES avatar(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS monologue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scene_id INTEGER NOT NULL,
    title TEXT,
    FOREIGN KEY (scene_id) REFERENCES scene(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS monologue_line (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monologue_id INTEGER NOT NULL,
    voice_profile_id INTEGER NOT NULL,
    line_order INTEGER NOT NULL,
    text TEXT NOT NULL,
    audio_path TEXT,
    generation_note TEXT,
    FOREIGN KEY (monologue_id) REFERENCES monologue(id) ON DELETE CASCADE,
    FOREIGN KEY (voice_profile_id) REFERENCES voice_profile(id) ON DELETE CASCADE,
    UNIQUE (monologue_id, line_order)
);