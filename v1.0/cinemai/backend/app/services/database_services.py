# backend/app/services/database_services.py

import logging

import sqlite3
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseServices:
    def __init__(self, db_path: str, sql_dir: str) -> None:
        self.db_path = db_path
        self.sql_dir = Path(sql_dir)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_sql_file(self, filename: str) -> None:
        file_path = self.sql_dir / filename
        sql = file_path.read_text(encoding="utf-8")
        with self.get_connection() as conn:
            conn.executescript(sql)

    def create_tables(self) -> None:
        logger.info("Creating Database")
        self.execute_sql_file("create_tables.sql")

    def fill_tables(self) -> None:
        logger.info("Filling Database")
        self.execute_sql_file("fill_tables.sql")

    def is_actress_table_empty(self) -> bool:
        with self.get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM actress").fetchone()
            return row["count"] == 0

    def get_avatar_by_name(self, name: str) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT av.id, av.name, av.actress_id, a.name AS actress_name
                FROM avatar av
                JOIN actress a ON a.id = av.actress_id
                WHERE av.name = ?
                """,
                (name,),
            ).fetchone()
            return dict(row) if row else None

    def get_avatar_by_id(self, avatar_id: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT av.id, av.name, av.actress_id, a.name AS actress_name
                FROM avatar av
                JOIN actress a ON a.id = av.actress_id
                WHERE av.id = ?
                """,
                (avatar_id,),
            ).fetchone()
            return dict(row) if row else None

    def get_scene_by_number(self, scene_number: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM scene
                WHERE scene_number = ?
                """,
                (scene_number,),
            ).fetchone()
            return dict(row) if row else None

    def get_scene_by_id(self, scene_id: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM scene
                WHERE id = ?
                """,
                (scene_id,),
            ).fetchone()
            return dict(row) if row else None

    def create_voice_profile(
        self,
        avatar_id: int,
        audio_reference_path: str,
        note: str | None,
        prompt_voice_clone_json: str,
    ) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO voice_profile (
                    avatar_id,
                    audio_reference_path,
                    note,
                    prompt_voice_clone_json
                )
                VALUES (?, ?, ?, ?)
                """,
                (avatar_id, audio_reference_path, note, prompt_voice_clone_json),
            )
            return cursor.lastrowid

    def get_voice_profile_by_id(self, voice_profile_id: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT vp.*, av.name AS avatar_name
                FROM voice_profile vp
                JOIN avatar av ON av.id = vp.avatar_id
                WHERE vp.id = ?
                """,
                (voice_profile_id,),
            ).fetchone()
            return dict(row) if row else None

    def create_monologue(
        self,
        scene_id: int,
        title: str | None = None,
    ) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO monologue (scene_id, title)
                VALUES (?, ?)
                """,
                (scene_id, title),
            )
            return cursor.lastrowid

    def get_monologue_by_id(self, monologue_id: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT m.*, s.scene_number
                FROM monologue m
                JOIN scene s ON s.id = m.scene_id
                WHERE m.id = ?
                """,
                (monologue_id,),
            ).fetchone()
            return dict(row) if row else None

    def create_monologue_line(
        self,
        monologue_id: int,
        voice_profile_id: int,
        line_order: int,
        text: str,
        audio_path: str | None = None,
        generation_note: str | None = None,
    ) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO monologue_line (
                    monologue_id,
                    voice_profile_id,
                    line_order,
                    text,
                    audio_path,
                    generation_note
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    monologue_id,
                    voice_profile_id,
                    line_order,
                    text,
                    audio_path,
                    generation_note,
                ),
            )
            return cursor.lastrowid

    def get_monologue_line_by_id(self, line_id: int) -> dict | None:
        with self.get_connection() as conn:
            row = conn.execute(
                """
                SELECT ml.*, vp.avatar_id, av.name AS avatar_name
                FROM monologue_line ml
                JOIN voice_profile vp ON vp.id = ml.voice_profile_id
                JOIN avatar av ON av.id = vp.avatar_id
                WHERE ml.id = ?
                """,
                (line_id,),
            ).fetchone()
            return dict(row) if row else None

    def update_monologue_line_audio_path(
        self,
        line_id: int,
        audio_path: str,
    ) -> None:
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE monologue_line
                SET audio_path = ?
                WHERE id = ?
                """,
                (audio_path, line_id),
            )