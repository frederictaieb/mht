from app.db.database import get_connection


def get_all_characters_with_actress():
    query = """
    SELECT c.name AS character, a.name AS actress
    FROM character c
    JOIN actress a ON a.id = c.actress_id
    ORDER BY a.name, c.name;
    """
    conn = get_connection()
    try:
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_characters_by_scene(scene_number: int):
    query = """
    SELECT s.scene_number, c.name AS character, a.name AS actress
    FROM scene_presence sp
    JOIN scene s ON s.id = sp.scene_id
    JOIN character c ON c.id = sp.character_id
    JOIN actress a ON a.id = c.actress_id
    WHERE s.scene_number = ?
    ORDER BY c.name;
    """
    conn = get_connection()
    try:
        rows = conn.execute(query, (scene_number,)).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_scenes_by_actress(actress_name: str):
    query = """
    SELECT a.name AS actress, c.name AS character, s.scene_number
    FROM scene_presence sp
    JOIN character c ON c.id = sp.character_id
    JOIN actress a ON a.id = c.actress_id
    JOIN scene s ON s.id = sp.scene_id
    WHERE a.name = ?
    ORDER BY s.scene_number, c.name;
    """
    conn = get_connection()
    try:
        rows = conn.execute(query, (actress_name,)).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_character_count_by_scene():
    query = """
    SELECT s.scene_number, COUNT(*) AS nb_characters
    FROM scene_presence sp
    JOIN scene s ON s.id = sp.scene_id
    GROUP BY s.scene_number
    ORDER BY s.scene_number;
    """
    conn = get_connection()
    try:
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_scene_count_by_actress():
    query = """
    SELECT a.name AS actress, COUNT(DISTINCT sp.scene_id) AS nb_scenes
    FROM scene_presence sp
    JOIN character c ON c.id = sp.character_id
    JOIN actress a ON a.id = c.actress_id
    GROUP BY a.id, a.name
    ORDER BY nb_scenes DESC, a.name;
    """
    conn = get_connection()
    try:
        rows = conn.execute(query).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()